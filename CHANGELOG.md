# Changelog

## v1.3 — Natural voices and audio preview (November 2026)

- Added **optional local Kokoro ONNX** voice generation with 10 selectable natural voices and speaking-speed control.
- Created a separate Python 3.12 voice environment that works alongside the user's Python 3.14 Streamlit environment.
- Added a **Preview voice only** button to avoid rendering a whole video just to hear a voice.
- Expanded Edge TTS fallback voices and changed the default rate to 0% (instead of +8%).
- Added a model downloader pinned to official GitHub release assets with SHA-256 verification.
- Added `docs/NATURAL_VOICES.md`, optional voice dependencies and mocked voice tests.
- Kept existing video layouts, user-recorded narration, and explicit review before publishing.
- Limitation: Kokoro captions are estimated, not forced-aligned. The model is not bundled with the repository.


## 1.2.0 — 2026-11-10
- Added **upload your own recorded narration** (MP3/WAV/M4A) as an alternative to online AI TTS.
- Accept an uploaded aligned SRT for own audio, or generate clearly labeled **approximate** word-timed captions from the supplied script.
- Added tests for estimated-caption generation; offline suite now contains 32 passing tests.
- Completed README, architecture, Windows installation, release checklist, rights/monetization, YouTube OAuth, portfolio and GitHub publishing documentation.

## 1.1.0 — 2026-11-10
- Refactored media logic into `shorts_core.py` to make it independently testable.
- Added timestamp and URL validation, local clip duration checking and downloadable SRT files.
- Added offline rendering smoke tests, CI workflow, demo footage generator and GitHub documentation.
- Kept optional Google OAuth uploader with manual confirmation and Private-by-default uploads.
- Added privacy/copyright warnings; no automatic publication.

## 1.0.0 — Original starter
- Initial Streamlit UI with source footage, optional B-roll, AI narration and captions.
