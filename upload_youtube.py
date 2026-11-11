"""Optional, consent-based YouTube uploader. Default uploads PRIVATE.
Google Cloud desktop OAuth credentials saved locally as client_secrets.json.
Never upload other people's videos without sufficient rights.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime, timezone
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE = Path(__file__).resolve().parent
SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]


def authorize():
    tokenfile = BASE / "token.json"
    secrets = BASE / "client_secrets.json"
    if not secrets.exists():
        raise SystemExit("Place the Google Cloud Desktop OAuth download at client_secrets.json. See README.md")
    creds = None
    if tokenfile.exists():
        creds = Credentials.from_authorized_user_file(str(tokenfile), SCOPE)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(secrets), SCOPE)
        creds = flow.run_local_server(port=0)
    tokenfile.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def main():
    parser = argparse.ArgumentParser(description="Upload reviewed Short using the official YouTube API")
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--publish-at", default="", help="ISO 8601 timestamp with timezone, e.g. 2026-11-20T16:00:00-05:00. Scheduling requires private upload.")
    parser.add_argument("--made-for-kids", action="store_true", help="Select only if the content is actually made for children")
    args = parser.parse_args()
    path = Path(args.file).resolve()
    if not path.is_file():
        parser.error("Cannot find video file")
    status = {"privacyStatus": args.privacy, "selfDeclaredMadeForKids": args.made_for_kids}
    if args.publish_at:
        if args.privacy != "private":
            parser.error("Use --privacy private with --publish-at")
        dt = datetime.fromisoformat(args.publish_at.replace("Z", "+00:00"))
        if dt.tzinfo is None or dt.utcoffset() is None:
            parser.error("--publish-at must include a timezone")
        if dt <= datetime.now(timezone.utc):
            parser.error("--publish-at must be in the future")
        status["publishAt"] = dt.isoformat()
    print(f"Ready to upload: {path.name}\nTitle: {args.title}\nPrivacy: {args.privacy}\nScheduled: {args.publish_at or 'No'}")
    if input("Type UPLOAD to confirm: ").strip() != "UPLOAD":
        raise SystemExit("Canceled")
    youtube = authorize()
    body = {"snippet": {"title": args.title, "description": args.description, "categoryId": "20"}, "status": status}
    media = MediaFileUpload(str(path), mimetype="video/mp4", resumable=True, chunksize=1024*1024*8)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        progress, response = request.next_chunk()
        if progress:
            print(f"Uploaded {progress.progress()*100:.0f}%")
    print("Uploaded:", "https://www.youtube.com/watch?v=" + response["id"])


if __name__ == "__main__":
    main()
