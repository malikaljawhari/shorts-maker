# Uploading reviewed Shorts to YouTube

## Recommended: YouTube Studio

1. Sign in at https://studio.youtube.com/.
2. Click **Create → Upload videos** and select the completed MP4 from `outputs/`.
3. Enter an accurate title, description, source acknowledgments, and any required disclosures. Choose the audience accurately.
4. Upload as **Private** the first time. Review YouTube's restrictions/checks and inspect the entire video, including on mobile.
5. Publish or schedule after checking editing, rights, claims, music and factual accuracy. No tool can promise monetization eligibility.

## Optional YouTube Data API v3

This project contains an **optional, separate** uploader, `upload_youtube.py`. It requires OAuth credentials, does not read your YouTube password, and **prompts before every upload**.

1. Create a project in https://console.cloud.google.com/ (use an account you're authorized to manage).
2. Enable **YouTube Data API v3** in API Library.
3. Set up the Google Auth Platform / OAuth consent screen; if testing, add your account as a test user where required.
4. Create OAuth client credentials of **Desktop app** type. Download JSON and save in the project folder as `client_secrets.json`.
5. Keep `client_secrets.json` and the subsequently created `token.json` private. They are excluded by `.gitignore`; never manually upload them.
6. With virtual environment installed, enter:

```powershell
.\.venv\Scripts\python.exe upload_youtube.py --file "outputs\ACTUAL_FILENAME.mp4" --title "My original gaming analysis" --description "Original analysis using footage I am permitted to use." --privacy private
```

7. Replace `ACTUAL_FILENAME.mp4` with the filename in the `outputs` folder. The browser opens for OAuth if needed. Confirm correct Google account and selected YouTube channel. The terminal asks you to type `UPLOAD` before transferring anything.
8. Review the private upload in YouTube Studio. Some projects' API uploads may be limited by verification, quota, API policy or channel settings. Manual Studio upload is a reliable alternative.

**Scheduling** (optional; use a future time with timezone):

```powershell
.\.venv\Scripts\python.exe upload_youtube.py --file "outputs\ACTUAL_FILENAME.mp4" --title "My original gaming analysis" --privacy private --publish-at "2026-11-20T16:00:00-05:00"
```

The scheduled upload remains private until its scheduled release. Scheduling and publishing may have account or API restrictions. Do **not** use scheduled publication without reviewing the content beforehand.

## Age, monetization and disclosures

The YouTube upload process and monetization process are different. If the channel owner is under 18, eligible monetization requires an approved **parent/guardian's AdSense for YouTube account**; do not misstate age or bypass verification. Some fan-funding features require adulthood independently. Follow current YouTube policies and the actual Google account restrictions.

Official documentation: [Data API upload guide](https://developers.google.com/youtube/data/guides/uploading_a_video), [YPP eligibility](https://support.google.com/youtube/answer/72851), [YouTube Studio](https://studio.youtube.com/).
