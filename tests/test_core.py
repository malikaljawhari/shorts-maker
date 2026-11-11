import io
from pathlib import Path

import pytest
from shorts_core import (
    MAX_DURATION, format_timestamp, parse_timestamp, save_upload,
    validate_range, youtube_url_allowed,
)


@pytest.mark.parametrize("input_,expected", [
    ("25", 25.0), ("00:25", 25.0), ("00:01:25", 85.0),
    ("1:02:03.500", 3723.5), (" 00:00:25 ", 25.0),
])
def test_parse_times(input_, expected):
    assert parse_timestamp(input_) == expected


@pytest.mark.parametrize("value", [
    "", "-1", "abc", "00:60", "00:00:60", "01:70:00", "00:00:05:00", "1.2345",
])
def test_reject_bad_times(value):
    with pytest.raises(ValueError):
        parse_timestamp(value)


def test_time_range():
    assert validate_range("00:00:05", "00:00:35") == (5, 35)
    for start, end in [("00:20", "00:20"), ("00:10", "00:08"), ("0", str(MAX_DURATION + 1))]:
        with pytest.raises(ValueError):
            validate_range(start, end)


def test_format_timestamp():
    assert format_timestamp(3723.5) == "01:02:03"
    with pytest.raises(ValueError):
        format_timestamp(-1)


@pytest.mark.parametrize("url", [
    "https://www.youtube.com/watch?v=abc", "https://youtube.com/shorts/abc",
    "https://m.youtube.com/watch?v=abc", "https://youtu.be/abcd",
])
def test_allowed_youtube_hosts(url):
    assert youtube_url_allowed(url)


@pytest.mark.parametrize("url", [
    "https://youtube.com.evil.test/watch?v=x", "https://notyoutube.com/watch?v=x",
    "http://youtube.com/watch?v=x", "https://youtube.com@evil.test/watch?v=x",
    "https://youtube.com:8000/watch?v=x", "file:///etc/passwd", "https://youtube.com/playlist?list=x",
])
def test_disallowed_youtube_hosts(url):
    assert not youtube_url_allowed(url)


def test_save_upload(tmp_path: Path):
    out = tmp_path / "source.mp4"
    assert save_upload(io.BytesIO(b"example"), out) == out
    assert out.read_bytes() == b"example"
    with pytest.raises(ValueError):
        save_upload(io.BytesIO(b"bad"), tmp_path / "sample.exe")


def test_estimated_word_subtitles(tmp_path: Path):
    from shorts_core import estimated_word_srt
    subs = estimated_word_srt("This is an original test script", 2.0, tmp_path / "words.srt")
    text = subs.read_text(encoding="utf-8")
    assert "THIS" in text and "SCRIPT" in text
    assert text.count(" --> ") == 6
    assert "00:00:02,000" in text
    with pytest.raises(ValueError):
        estimated_word_srt("hello", 0, subs)
