# Natural AI voices — local Kokoro setup (Windows)

Shorts Maker v1.3 adds **Kokoro ONNX**, a local speech generator. You do not need an API key or subscription. Its voice model weights are licensed under Apache-2.0 and the `kokoro-onnx` library is MIT licensed; check licenses before use. Voices are generated on your computer after a one-time download.

**Important:** the **official upstream** `kokoro-onnx==0.6.1` Python package supports Python 3.10–3.13, **not Python 3.14**. Keep the main `.venv` and its Python 3.14. Create a separate `.voice-venv` using Python 3.12; the app automatically calls it for Kokoro. Do not uninstall your current Python.

## First-time setup (five commands)

1. Install Python 3.12 alongside Python 3.14 from https://www.python.org/downloads/ or via:

   ```powershell
   winget install --id Python.Python.3.12 -e
   ```

   Then close and reopen PowerShell. Verify: `py -3.12 --version`. If no 3.12 interpreter appears, restart your computer and/or use the official Python installer.

2. Open File Explorer to the **inner extracted project folder**, containing `app.py` and `requirements-voices.txt`. Click the **address bar** (`Ctrl+L`), type `powershell`, and press Enter.

3. In that PowerShell window, run the following one line at a time:

   ```powershell
   py -3.12 -m venv .voice-venv
   .\.voice-venv\Scripts\python.exe -m pip install --upgrade pip
   .\.voice-venv\Scripts\python.exe -m pip install -r requirements-voices.txt
   python tools\download_kokoro_models.py
   ```

   The last command downloads ~140 MB of model and voice files from the official `thewh1teagle/kokoro-onnx` GitHub release into the **ignored** `models/` folder and verifies their published SHA-256 hashes. Download size, speed and storage use may vary.

4. Start the existing app (using **your original** `.venv`):

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

5. In Shorts Maker choose **Natural AI — Kokoro (offline)**, select **Michael**, **Heart**, or **George** (or any listed voice), enter a script, and click **Preview voice only**. Choose **Create MP4 + SRT** once you're happy with the preview.

**Voice engine setup is optional.** Edge TTS, uploaded narration and normal video rendering still work if Kokoro is not installed.

## Voice selection suggestions

| Voice | Style to test |
|---|---|
| Michael | American male gaming commentary |
| Adam | Deeper American male delivery |
| Heart | Warm American female narration |
| Sarah | Clear American female narration |
| Bella | Brighter American female delivery |
| Emma | British female narration |
| George | British male documentary style |

Actual results vary by script, pronunciation, speed and computer. Start at speed **1.00**; try 0.95 for more deliberate voiceover or 1.05 for more energy. Slowing/speeding too much can make voices less natural.

## Captions and important limitations

- **Kokoro currently uses estimated one-word timings** based on the text and final audio length. Captions are **not guaranteed to align to every spoken word**. Watch your video and revise the exported `.srt`, or upload a manually aligned SRT using the Recorded Voice mode for accurate captions. The older Edge TTS option uses service-provided word boundary timing.
- The first local generation may be slower, particularly on Windows CPU. No speech API charges; electricity and bandwidth still apply.
- Do not expose the locally running Streamlit app to the public internet as-is.
- The download helper only downloads two fixed official model release URLs, checks SHA-256, and never runs downloaded code.
- If you want to **uninstall just Kokoro**, you can delete `.voice-venv/` and `models/` after backing up your project. That does **not** delete your main app or its `.venv/` environment.
- The optional natural voices require model and library dependencies downloaded separately; they are deliberately excluded from GitHub to keep the repository light.

## Common errors

**`No module named kokoro_onnx`**: Verify `py -3.12 --version` and reinstall `requirements-voices.txt` into `.voice-venv`, not `.venv`.

**`Kokoro model file is missing`**: Run `python tools\download_kokoro_models.py` inside the correct project folder with internet access. On a checksum mismatch delete the partial or corrupted file and retry.

**`Python 3.14 needs ... .voice-venv`**: The official library does not install into Python 3.14; use the separate Python 3.12 environment as above.

**Slow rendering**: Generating local voices uses CPU and can be slow on older systems. Preview a short sample before generating full narration.

**Captions don't sync**: Kokoro timestamps are estimates. Use an accurately aligned SRT rather than assuming your captions match the sound.

## Source / license information

- Library documentation: https://github.com/thewh1teagle/kokoro-onnx
- Official model release and hashes: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1
- Kokoro model card: https://huggingface.co/hexgrad/Kokoro-82M

The separate model files are not part of this repository's MIT license.
