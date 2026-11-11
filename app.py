"""Streamlit user interface for the locally-running Shorts Maker."""
from __future__ import annotations

import asyncio
import shutil
import tempfile
import uuid
from pathlib import Path

import streamlit as st
from natural_voice import KOKORO_VOICES, make_kokoro_voice, voice_ready
from shorts_core import (
    VOICE_IDS, authorized_youtube_clip, clip_local, duration, ensure_tools,
    estimated_word_srt, make_voice, render_video, save_upload,
    validate_range, youtube_url_allowed,
)

PROJECT = Path(__file__).resolve().parent
OUTPUTS = PROJECT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="Shorts Maker", page_icon="🎬", layout="centered")
st.title("🎬 Shorts Maker")
st.caption("Turn footage you're permitted to use into a narrated 9:16 video with word-by-word captions.")
st.info(
    "Use footage you own or are authorized to download and reuse. Narration, cropping, and subtitles "
    "do not automatically establish fair use. The app exports videos locally; it does not publish them."
)

with st.expander("What does this app actually automate?"):
    st.write(
        "It trims a source video, prepares optional background footage, uses online AI narration or your "
        "own recorded narration, and adds captions. It renders a 1080×1920 MP4. You choose the script, footage and "
        "timestamps. The original footage's audio is muted. Review every output before uploading."
    )

with st.form("video_form"):
    st.subheader("1. Main video")
    source_mode = st.radio("Video source", ["Upload video", "Paste an authorized YouTube link"], horizontal=True)
    source_upload = None
    source_url = ""
    if source_mode == "Upload video":
        source_upload = st.file_uploader("Upload an MP4/MOV/WEBM/MKV", type=["mp4", "mov", "webm", "mkv"])
    else:
        source_url = st.text_input("Authorized YouTube link", placeholder="https://www.youtube.com/watch?v=...")
    ca, cb = st.columns(2)
    start = ca.text_input("Clip start", value="00:00:00", help="HH:MM:SS")
    end = cb.text_input("Clip end", value="00:00:25", help="HH:MM:SS; up to three minutes")

    st.subheader("2. Video layout")
    layout = st.radio("Layout", ["Split-screen", "Blurred background"], horizontal=True)
    broll_upload = None
    broll_url = ""
    ba, bb = "00:00:00", "00:00:45"
    if layout == "Split-screen":
        background_mode = st.radio("Gameplay background", ["Upload B-roll", "Paste authorized B-roll link"], horizontal=True)
        if background_mode == "Upload B-roll":
            broll_upload = st.file_uploader("Upload gameplay/background video", type=["mp4", "mov", "webm", "mkv"])
        else:
            broll_url = st.text_input("Authorized B-roll YouTube link")
            col_a, col_b = st.columns(2)
            ba = col_a.text_input("B-roll start", value=ba)
            bb = col_b.text_input("B-roll end", value=bb)

    st.subheader("3. Voiceover and captions")
    script = st.text_area(
        "Original narration script", height=180,
        placeholder="What surprised me about this gameplay is...",
        help="Check every factual claim. For recorded narration, enter words matching your audio.",
    )
    narration_mode = st.radio(
        "Narration source",
        ["Natural AI — Kokoro (offline)", "Edge TTS (online / experimental)", "Upload my own voice"],
        help="Kokoro runs locally after optional installation. Edge TTS is retained for testing.",
    )
    voice = ""
    speed = 0
    kokoro_voice = next(iter(KOKORO_VOICES))
    kokoro_speed = 1.0
    own_audio = None
    own_srt = None
    if narration_mode == "Natural AI — Kokoro (offline)":
        kokoro_voice = st.selectbox("Natural voice", list(KOKORO_VOICES))
        kokoro_speed = st.slider("Speaking speed", 0.80, 1.20, 1.00, step=0.05)
        status, status_text = voice_ready()
        if status:
            st.success("Local Kokoro assets found. Ready for a voice preview or render.")
        else:
            st.warning(status_text)
            st.caption("Install the optional voice environment following docs/NATURAL_VOICES.md. "
                       "Your existing Edge TTS and video tools will continue to work.")
        st.caption("Kokoro subtitles are initially **estimated from the script**, not precisely speech-aligned. "
                   "Check timing carefully before publishing.")
    elif narration_mode == "Edge TTS (online / experimental)":
        voice = st.selectbox("Edge narration voice", list(VOICE_IDS), index=1)
        speed = st.slider("Voice speed adjustment (%)", -20, 30, 0, step=2)
        st.caption("Uses an unofficial online edge-tts service. Verify usage terms before commercial publishing.")
    else:
        own_audio = st.file_uploader(
            "Upload your narration (MP3/WAV/M4A)", type=["mp3", "wav", "m4a"], key="my_audio",
        )
        own_srt = st.file_uploader(
            "Optional precisely timed SRT captions", type=["srt"], key="my_srt",
        )
        st.caption("Without an SRT, word timings are estimates, not verified transcription. Review them.")
    rights = st.checkbox(
        "I own or am permitted to reuse all footage; for any link, I also have permission "
        "under the source platform's download rules."
    )
    preview = st.form_submit_button("Preview voice only (short sample)")
    generate = st.form_submit_button("Create MP4 + SRT", type="primary", use_container_width=True)

if preview:
    try:
        if narration_mode == "Upload my own voice":
            if own_audio is None:
                raise ValueError("Upload your narration first")
            st.audio(own_audio.getvalue(), format="audio/mpeg" if own_audio.name.lower().endswith("mp3") else "audio/wav")
        else:
            if len(script.strip().split()) < 3:
                raise ValueError("Enter a narration script first")
            sample = " ".join(script.strip().split()[:22])
            with st.spinner("Generating a short voice preview…"):
                with tempfile.TemporaryDirectory(prefix="shorts_voice_preview_") as temp:
                    work = Path(temp)
                    if narration_mode == "Natural AI — Kokoro (offline)":
                        audio, _ = make_kokoro_voice(sample, KOKORO_VOICES[kokoro_voice], kokoro_speed, work)
                    else:
                        audio, _ = asyncio.run(make_voice(sample, VOICE_IDS[voice], speed, work))
                    st.session_state["shorts_voice_preview"] = (audio.read_bytes(), audio.suffix.lower())
            st.success("Voice preview ready — listen before rendering a whole video")
    except Exception as exc:
        st.error(f"Voice preview failed: {exc}")
if "shorts_voice_preview" in st.session_state:
    clip, suffix = st.session_state["shorts_voice_preview"]
    st.audio(clip, format="audio/wav" if suffix == ".wav" else "audio/mpeg")

if generate:
    try:
        if not rights:
            raise ValueError("Confirm footage rights and platform download permissions first")
        ensure_tools()
        a, b = validate_range(start, end)
        if len(script.split()) < 5:
            raise ValueError("Enter at least five words of original commentary")
        if narration_mode == "Upload my own voice" and own_audio is None:
            raise ValueError("Upload your MP3, WAV or M4A narration")
        if source_mode == "Upload video" and source_upload is None:
            raise ValueError("Please upload your source footage")
        if source_mode != "Upload video" and not youtube_url_allowed(source_url):
            raise ValueError("Enter a supported HTTPS YouTube source link")
        if layout == "Split-screen" and broll_upload is None and not youtube_url_allowed(broll_url):
            raise ValueError("Split-screen requires background footage")

        with st.spinner("Preparing footage, narration, captions and video…"):
            with tempfile.TemporaryDirectory(prefix="shorts_maker_") as temp:
                work = Path(temp)
                if source_upload is not None:
                    filename = "source" + Path(source_upload.name).suffix.lower()
                    main = save_upload(source_upload, work / filename)
                    foreground = clip_local(main, a, b, work)
                else:
                    foreground = authorized_youtube_clip(source_url, a, b, work, "source")
                background = None
                if layout == "Split-screen":
                    if broll_upload is not None:
                        filename = "broll" + Path(broll_upload.name).suffix.lower()
                        background = save_upload(broll_upload, work / filename)
                    else:
                        c, d = validate_range(ba, bb)
                        background = authorized_youtube_clip(broll_url, c, d, work, "background")
                if narration_mode == "Natural AI — Kokoro (offline)":
                    narration, subs = make_kokoro_voice(
                        script.strip(), KOKORO_VOICES[kokoro_voice], kokoro_speed, work,
                    )
                elif narration_mode == "Edge TTS (online / experimental)":
                    narration, subs = asyncio.run(make_voice(script.strip(), VOICE_IDS[voice], speed, work))
                else:
                    narration = work / ("narration" + Path(own_audio.name).suffix.lower())
                    with narration.open("wb") as audio_file:
                        audio_file.write(own_audio.getbuffer())
                    sound_duration = duration(narration)
                    if sound_duration > 180:
                        raise ValueError("Narration must be three minutes or shorter")
                    subs = work / "words.srt"
                    if own_srt is not None:
                        subs.write_bytes(own_srt.getvalue())
                        if not subs.read_text(encoding="utf-8-sig").strip():
                            raise ValueError("Caption file is empty")
                    else:
                        estimated_word_srt(script.strip(), sound_duration, subs)
                stem = "short_" + uuid.uuid4().hex[:10]
                video_path = OUTPUTS / (stem + ".mp4")
                srt_path = OUTPUTS / (stem + ".srt")
                render_video(foreground, background, narration, subs, layout, video_path, work)
                shutil.copyfile(subs, srt_path)

        st.success("Export complete! Watch the entire video and verify subtitles before uploading.")
        st.video(str(video_path))
        col1, col2 = st.columns(2)
        col1.download_button(
            "Download MP4", data=video_path.read_bytes(), file_name=video_path.name,
            mime="video/mp4", use_container_width=True,
        )
        col2.download_button(
            "Download captions (.srt)", data=srt_path.read_bytes(), file_name=srt_path.name,
            mime="application/x-subrip", use_container_width=True,
        )
        st.caption(f"Saved on your computer: {video_path}")
        st.warning("Human review required: verify sources/rights, audio, accuracy, captions and YouTube policy compliance.")
    except Exception as error:
        st.error(f"Could not render this video: {error}")
        st.caption("See docs/TROUBLESHOOTING.md. URL mode may fail if the platform changes or blocks the request.")

st.divider()
st.caption("Open-source local video editor. No voice models or third-party media are bundled with the repository.")
