"""Generate synthetic video backgrounds you can freely test with; not copyrighted gameplay."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "demo_media"
OUT.mkdir(exist_ok=True)
if not shutil.which("ffmpeg"):
    raise SystemExit("Install FFmpeg and restart the terminal first")

samples = {
    "demo_source.mp4": "testsrc2=size=1280x720:rate=25:duration=12",
    "demo_background.mp4": "color=c=darkslateblue:s=1280x720:r=25:d=12",
}
for filename, filter_ in samples.items():
    out = OUT / filename
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", filter_,
        "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast", out.as_posix(),
    ], check=True)
    print("Created", out)
print("These generated test videos contain no third-party gameplay.")
