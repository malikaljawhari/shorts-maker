# Testing and release checklist

## Tests (from the project root)

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

Current offline test suite includes: timestamp parsing, invalid timestamps/ranges, URL host validation, upload extension checks, approximate SRT creation, real FFmpeg test-clip extraction, real FFmpeg split-screen export, real FFmpeg blurred-background export, and missing-B-roll errors. **32 tests passed** on a Linux FFmpeg/Python test environment at project preparation. Windows and live online services require local verification. Some render tests skip if FFmpeg is unavailable.

## Offline demo footage

```powershell
.\.venv\Scripts\python.exe tools/create_demo_footage.py
```

The tool generates an original synthetic 12-second color/test-pattern video and a background in `demo_media/`. Use source range `00:00:00` → `00:00:10` in the GUI. **Do not claim this is gameplay footage**. Choose an owned narration file or AI voice to complete the export.

## Manual release checklist

- [ ] Test opening localhost from PowerShell in the correct folder
- [ ] Test main video upload and trimming shorter than source duration
- [ ] Test authorized URL mode only with your own/authorized video
- [ ] Test split-screen and blurred layouts
- [ ] Test original narration MP3 + SRT and the estimated-caption fallback
- [ ] Test online AI voice only after verifying your intended use's licensing
- [ ] Watch entire exported MP4 on PC and phone: sound, alignment, cropping, safe captions
- [ ] Keep credentials/videos/private analytics outside Git
- [ ] Upload first completed video **Private** in YouTube Studio
- [ ] Verify content rights, metadata, copyright notices and audience setting
- [ ] Run tests after changes and inspect GitHub Actions results

## Not tested automatically

Live `edge-tts`, third-party URLs, your Google OAuth account, YouTube uploads, real content ownership, accuracy of scripts, and eligibility for commercial monetization. These are service/account-specific and require manual tests.


## v1.3 test scope

`tests/test_natural_voice.py` validates voice IDs, missing-model handling, Python 3.14 compatibility messages, invalid script/speed rejection, and the worker's API call shape with mocked Kokoro modules. These tests do **not** prove natural voice quality, runtime performance, or accurate captions. Complete a real local preview after installing Python 3.12, the optional dependencies, and official model files.
