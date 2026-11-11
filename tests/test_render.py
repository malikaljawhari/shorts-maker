"""Offline smoke tests of video editing with synthetic footage."""
import shutil
import subprocess
from pathlib import Path

import pytest
from shorts_core import clip_local, duration, render_video


pytestmark = pytest.mark.skipif(
    not shutil.which("ffmpeg") or not shutil.which("ffprobe"),
    reason="FFmpeg executables not installed",
)


def run_ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


@pytest.fixture
def assets(tmp_path: Path):
    source = tmp_path / "source.mp4"
    broll = tmp_path / "broll.mp4"
    narration = tmp_path / "narration.mp3"
    subs = tmp_path / "words.srt"
    run_ffmpeg("-f", "lavfi", "-i", "color=c=blue:s=320x180:r=25:d=1.5", "-pix_fmt", "yuv420p", source)
    run_ffmpeg("-f", "lavfi", "-i", "color=c=green:s=320x180:r=25:d=1.5", "-pix_fmt", "yuv420p", broll)
    run_ffmpeg("-f", "lavfi", "-i", "sine=frequency=440:duration=1.2", "-q:a", "3", narration)
    subs.write_text("1\n00:00:00,000 --> 00:00:01,000\nHELLO\n", encoding="utf-8")
    return source, broll, narration, subs


def test_local_clip(assets, tmp_path):
    source, *_ = assets
    clipped = clip_local(source, 0, 1.0, tmp_path)
    assert clipped.exists()
    assert 0.8 <= duration(clipped) <= 1.2
    with pytest.raises(ValueError):
        clip_local(source, 5, 6, tmp_path)


@pytest.mark.parametrize("layout", ["Split-screen", "Blurred background"])
def test_render_video_offline(assets, tmp_path, layout):
    source, broll, narration, subs = assets
    output = tmp_path / f"out_{layout.replace(' ', '_')}.mp4"
    render_video(source, broll if layout == "Split-screen" else None, narration, subs, layout, output, tmp_path, width=360)
    assert output.stat().st_size > 1000
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
        "-of", "csv=s=x:p=0", str(output),
    ], text=True).strip()
    assert probe == "360x640"
    assert duration(output) >= 1.0


def test_render_missing_background(assets, tmp_path):
    source, _, narration, subs = assets
    with pytest.raises(ValueError, match="background"):
        render_video(source, None, narration, subs, "Split-screen", tmp_path / "not.mp4", tmp_path, width=360)
