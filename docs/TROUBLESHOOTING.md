# Windows troubleshooting and upgrade

## You already have an older Shorts Maker running

In its PowerShell window press **Ctrl+C** to stop it. Leave the old folder and `outputs/` intact. Extract the new ZIP to a new directory. Open **the inner folder** containing `app.py` and `shorts_core.py`, use File Explorer **address bar** (`Ctrl+L`) → `powershell` → Enter. Set up the new `.venv` following `README.md`.

## `py` or `python` not recognized

Confirm `python --version`. Use `py -3.14` or install Python from python.org. Multiple Python versions may coexist. The environment needs to be made with a version where the dependencies can install.

## `The system cannot find the path specified` for `.venv\Scripts\python.exe`

You are likely in the wrong folder or virtual environment was not created. Run `Get-Location`, check `dir` for `app.py`, then `python -m venv .venv`. If you accidentally created `.venv` in the **parent** folder for the old project, that is fine; for the new project create one inside the inner project folder.

## `ffmpeg not found` or `ffprobe not found`

Run `ffmpeg -version` and `ffprobe -version`. On Windows: `winget install --id Gyan.FFmpeg -e`, then close/reopen PowerShell. `pip install ffmpeg` does **not** install the needed FFmpeg executable.

## Browser page blank / port 8501 occupied

`Ctrl+C` to stop any prior Streamlit server. Re-run `...python.exe -m streamlit run app.py`. Or start on a different port: `... -m streamlit run app.py --server.port 8502` and open `http://localhost:8502`.

## `No such filter: subtitles`

FFmpeg was built without `libass`. Install a complete FFmpeg build supporting its `subtitles` filter. Check `ffmpeg -filters` for `subtitles`.

## Error about source duration

The clip end timestamp exceeds the length of your uploaded footage; choose a shorter end time. A 12-second demo clip cannot use a 25-second end timestamp.

## AI narration fails

The `edge-tts` backend needs internet and is unofficial. The service can change; try again later or use **Upload my own voice** plus an SRT. This app does not promise voice-service commercial rights.

## Word captions do not match your own recorded narration

Own-voice mode without an uploaded SRT **estimates** when to display words. You need to provide an aligned SRT (from an editor/transcriber whose usage rules you follow), or adjust captions afterward. Also ensure the pasted script matches the spoken audio.

## URL fails to download

Link processing can fail due to YouTube changes, video unavailability or platform restrictions. Use a locally provided file you are legally allowed to use. **Do not** bypass restrictions, authentication or DRM.

## Slow renders / big files

Rendering at 1080×1920 uses significant CPU. Use shorter excerpts and close other intensive programs; do not upload hours of raw source when a permitted shorter MP4 is available. Video uploads are capped by Streamlit config, currently 200 MB each.

## `ImportError` on Python 3.14

Update pip and dependencies. If a third-party package does not support Python 3.14 yet, install Python 3.12 **alongside** your existing Python and build a new environment: `py -3.12 -m venv .venv` after renaming/moving the incompatible one. Do not uninstall working Python 3.14.

## YouTube API authentication fails

Read `docs/YOUTUBE_UPLOAD.md`. Check Google Cloud project, OAuth consent and test users, quotas, correct account/channel and API restrictions. Never paste OAuth JSON or tokens into GitHub issues.
