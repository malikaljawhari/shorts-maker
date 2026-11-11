"""Reusable, testable video production functions for the Shorts Maker GUI.

Clips must be owned or available for reuse *and* download under source-platform rules.
Neither cropping nor adding narration automatically establishes copyright permission.
"""
from __future__ import annotations

import asyncio
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

VOICE_IDS = {
    "US English — Christopher": "en-US-ChristopherNeural",
    "US English — Guy": "en-US-GuyNeural",
    "US English — Aria": "en-US-AriaNeural",
    "US English — Jenny": "en-US-JennyNeural",
    "US English — Eric": "en-US-EricNeural",
    "UK English — Ryan": "en-GB-RyanNeural",
}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}
MAX_DURATION = 180


def command(args: list[str], cwd: Path | None = None) -> str:
    """Run a local process without a shell (prevents command string injection)."""
    completed = subprocess.run(
        args, cwd=str(cwd) if cwd else None,
        text=True, capture_output=True, errors="replace", check=False,
    )
    if completed.returncode:
        output = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(f"{Path(args[0]).name} failed ({completed.returncode}):\n{output[-1800:]}")
    return completed.stdout


def parse_timestamp(value: str) -> float:
    """Return seconds from SS[.ms], MM:SS[.ms] or HH:MM:SS[.ms]."""
    raw = value.strip()
    if not re.fullmatch(r"\d+(?::\d{1,2}){0,2}(?:\.\d{1,3})?", raw):
        raise ValueError("Time must look like 25, 00:25, or 00:00:25")
    parts = raw.split(":")
    if len(parts) > 1 and (float(parts[-1]) >= 60 or (len(parts) == 3 and int(parts[-2]) >= 60)):
        raise ValueError("Seconds and minutes components must be under 60")
    total = 0.0
    for part in parts:
        total = total * 60 + float(part)
    return total


def format_timestamp(sec: float) -> str:
    if sec < 0:
        raise ValueError("Time cannot be negative")
    whole = int(sec)
    return f"{whole // 3600:02}:{(whole % 3600) // 60:02}:{whole % 60:02}"


def validate_range(start: str, end: str, max_seconds: float = MAX_DURATION) -> tuple[float, float]:
    a, b = parse_timestamp(start), parse_timestamp(end)
    if b <= a or b - a > max_seconds:
        raise ValueError(f"End must be after start; select at most {max_seconds:g} seconds")
    return a, b


def youtube_url_allowed(url: str) -> bool:
    """Check HTTPS YouTube hostnames; this does NOT grant usage rights."""
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return False
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or parsed.port not in (None, 443):
        return False
    if parsed.username or parsed.password:
        return False
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        return parsed.path.startswith(("/watch", "/shorts/", "/live/"))
    if host in {"youtu.be", "www.youtu.be"}:
        return bool(parsed.path.strip("/"))
    return False


def ensure_tools() -> None:
    missing = [name for name in ("ffmpeg", "ffprobe") if not shutil.which(name)]
    if missing:
        raise RuntimeError(f"Missing {', '.join(missing)} on PATH. Install FFmpeg and reopen PowerShell")


def duration(media_path: Path) -> float:
    raw = command([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(media_path),
    ]).strip()
    try:
        result = float(raw)
    except ValueError as exc:
        raise ValueError("Cannot read media duration; try converting the file to MP4") from exc
    if not 0 < result < 86400 * 10:
        raise ValueError("Invalid media duration")
    return result


def save_upload(upload, path: Path) -> Path:
    if path.suffix.lower() not in VIDEO_EXTENSIONS:
        raise ValueError("Unsupported video extension")
    with path.open("wb") as fh:
        shutil.copyfileobj(upload, fh)
    return path


def authorized_youtube_clip(url: str, start: float, end: float, work: Path, prefix: str) -> Path:
    if not youtube_url_allowed(url):
        raise ValueError("Enter a supported HTTPS YouTube video link")
    if end <= start or end - start > MAX_DURATION:
        raise ValueError("Invalid clip timestamp range")
    command([
        "yt-dlp", "--no-playlist", "--no-progress", "--no-overwrites",
        "--download-sections", f"*{format_timestamp(start)}-{format_timestamp(end)}",
        "--force-keyframes-at-cuts", "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
        "--merge-output-format", "mp4", "--remux-video", "mp4",
        "-o", f"{prefix}.%(ext)s", url.strip(),
    ], cwd=work)
    found = [p for p in work.glob(f"{prefix}.*") if p.suffix.lower() in VIDEO_EXTENSIONS]
    if len(found) != 1:
        raise RuntimeError("Could not retrieve a permitted video clip; use an authorized local file")
    return found[0]


def clip_local(source: Path, start: float, end: float, work: Path) -> Path:
    source_duration = duration(source)
    if start >= source_duration or end > source_duration + 0.25:
        raise ValueError(f"Clip range exceeds source duration ({source_duration:.1f} seconds)")
    target = work / "top.mp4"
    command([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", str(start), "-i", str(source), "-t", str(end-start),
        "-map", "0:v:0", "-an", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "22", "-pix_fmt", "yuv420p", str(target),
    ])
    return target


async def make_voice(script: str, voice: str, rate: int, work: Path) -> tuple[Path, Path]:
    """Create speech + word-boundary SRT using unofficial online edge-tts.

    Licensing/availability of the connected voice service must be verified before
    commercial use; this code does not provide a commercial license.
    """
    import edge_tts

    audio = work / "narration.mp3"
    subs = work / "words.srt"
    speech = edge_tts.Communicate(script, voice=voice, rate=f"{rate:+d}%", boundary="WordBoundary")
    maker = edge_tts.SubMaker()
    with audio.open("wb") as output:
        async for chunk in speech.stream():
            if chunk["type"] == "audio":
                output.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                item = dict(chunk)
                item["text"] = item["text"].upper()
                maker.feed(item)
    if audio.stat().st_size <= 100:
        raise RuntimeError("Narration not generated. Check internet connection and voice service")
    subs.write_text(maker.get_srt(), encoding="utf-8")
    if not subs.read_text(encoding="utf-8").strip():
        raise RuntimeError("No word timings returned by voice service; upgrade edge-tts")
    return audio, subs



def estimated_word_srt(script: str, total_seconds: float, destination: Path) -> Path:
    """Write approximate one-word captions for separately recorded narration.

    This does not analyze recorded speech. Captions must be reviewed and adjusted
    if audio and script do not match. Upload a pre-aligned SRT for accuracy.
    """
    words = script.strip().split()
    if not words or not 0.2 <= total_seconds <= MAX_DURATION + 1:
        raise ValueError("Need narration text and an audio track of at most three minutes")
    weights = [max(3, len(w.strip('.,!?;:\"\'()'))) for w in words]
    total_weight = sum(weights)

    def stamp(position: float) -> str:
        millis = max(0, round(position * 1000))
        hour, remainder = divmod(millis, 3_600_000)
        minute, remainder = divmod(remainder, 60_000)
        second, ms = divmod(remainder, 1000)
        return f"{hour:02}:{minute:02}:{second:02},{ms:03}"

    current = 0
    lines = []
    for index, (word, weight) in enumerate(zip(words, weights), start=1):
        following = current + weight
        start = total_seconds * current / total_weight
        end = total_seconds * following / total_weight
        # Escape ASS/HTML-lookalike punctuation in caption text.
        visible = re.sub(r"<[^>]*>", "", word).upper().replace("{", "(").replace("}", ")")
        lines.append(f"{index}\n{stamp(start)} --> {stamp(end)}\n{visible}\n")
        current = following
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination


def render_video(
    foreground: Path, background: Path | None, narration: Path, subtitles: Path,
    layout: str, output: Path, work: Path, *, width: int = 1080,
) -> None:
    """Render a Short with source audio muted and narration on the soundtrack."""
    if width <= 0 or width % 2:
        raise ValueError("Output width must be positive and even")
    if layout not in {"Split-screen", "Blurred background"}:
        raise ValueError("Unsupported layout")
    if layout == "Split-screen" and background is None:
        raise ValueError("Split-screen needs a background clip")
    height = width * 16 // 9
    half = height // 2
    if height % 2:
        raise ValueError("Output height must be even")
    font_size = max(12, width * 32 // 1080)
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-stream_loop", "-1", "-i", str(foreground)]
    if layout == "Split-screen":
        args.extend(["-stream_loop", "-1", "-i", str(background)])
        audio_idx = 2
        layers = (
            f"[0:v]scale={width}:{half}:force_original_aspect_ratio=increase,crop={width}:{half},setsar=1[top];"
            f"[1:v]scale={width}:{half}:force_original_aspect_ratio=increase,crop={width}:{half},setsar=1[bottom];"
            "[top][bottom]vstack=inputs=2[base];"
        )
    else:
        audio_idx = 1
        layers = (
            "[0:v]split=2[back][front];"
            f"[back]scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},boxblur=18:3[bg];"
            f"[front]scale={width}:{height}:force_original_aspect_ratio=decrease,setsar=1[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"
        )
    args += ["-i", str(narration)]
    # work/words.srt is a relative basename to avoid Windows drive-colon escaping issues.
    # ASS Alignment=5 is center; color codes are AABBGGRR.
    style = (f"Fontname=Arial,Fontsize={font_size},PrimaryColour=&H0000FFFF,"
             "OutlineColour=&H00000000,Bold=1,BorderStyle=1,Outline=3,Shadow=1,Alignment=5")
    filtergraph = layers + f"[base]subtitles=words.srt:force_style='{style}',fps=30,format=yuv420p[v]"
    args += [
        "-filter_complex", filtergraph, "-map", "[v]", "-map", f"{audio_idx}:a:0",
        "-t", str(duration(narration)), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", str(output),
    ]
    command(args, cwd=work)
    if not output.is_file() or output.stat().st_size < 1000:
        raise RuntimeError("The renderer did not produce a usable MP4")
