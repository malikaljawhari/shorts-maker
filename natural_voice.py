"""Local, optional Kokoro voice engine orchestration.

Streamlit can keep running on Python 3.14 while the Kokoro worker uses a
separate Python 3.12 virtual environment, because upstream kokoro-onnx 0.6.1
requires Python <3.14. No credentials or external TTS provider are needed.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from shorts_core import command, duration, estimated_word_srt

ROOT = Path(__file__).resolve().parent
MODELS = ROOT / 'models'
MODEL = MODELS / 'kokoro-v1.0.int8.onnx'
VOICES_FILE = MODELS / 'voices-v1.0.bin'
WORKER = ROOT / 'tools' / 'kokoro_worker.py'

KOKORO_VOICES = {
    'Heart — warm American voice': 'af_heart',
    'Sarah — clear American voice': 'af_sarah',
    'Bella — bright American voice': 'af_bella',
    'Nicole — calm American voice': 'af_nicole',
    'Michael — American male voice': 'am_michael',
    'Adam — deeper American male voice': 'am_adam',
    'Liam — American male voice': 'am_liam',
    'Emma — British female voice': 'bf_emma',
    'George — British male voice': 'bm_george',
    'Daniel — British male voice': 'bm_daniel',
}


def interpreter_path(root: Path = ROOT) -> Path:
    """Prefer optional Python 3.12 voice venv; otherwise current interpreter."""
    if sys.platform == 'win32':
        separate = root / '.voice-venv' / 'Scripts' / 'python.exe'
    else:
        separate = root / '.voice-venv' / 'bin' / 'python'
    if separate.is_file():
        return separate
    return Path(sys.executable)


def voice_ready(root: Path = ROOT) -> tuple[bool, str]:
    model = root / 'models' / MODEL.name
    voices = root / 'models' / VOICES_FILE.name
    if not model.is_file() or model.stat().st_size < 1_000_000:
        return False, 'Kokoro model file is missing. Follow docs/NATURAL_VOICES.md.'
    if not voices.is_file() or voices.stat().st_size < 1_000_000:
        return False, 'Kokoro voices file is missing. Follow docs/NATURAL_VOICES.md.'
    chosen = interpreter_path(root)
    if chosen == Path(sys.executable) and sys.version_info >= (3, 14):
        return False, 'Python 3.14 needs the optional Python 3.12 .voice-venv. See docs/NATURAL_VOICES.md.'
    return True, 'Kokoro files found. Voice engine availability is checked at generation time.'


def make_kokoro_voice(
    script: str, voice_id: str, speed: float, work: Path, *, root: Path = ROOT,
) -> tuple[Path, Path]:
    """Synthesize locally; write approximate SRT (Kokoro does not expose word alignment)."""
    if not script.strip() or len(script) > 5000:
        raise ValueError('Narration must contain between 1 and 5,000 characters')
    if voice_id not in KOKORO_VOICES.values():
        raise ValueError('Select an available Kokoro voice')
    if not 0.80 <= speed <= 1.20:
        raise ValueError('Kokoro speed must be from 0.80 to 1.20')
    ready, reason = voice_ready(root)
    if not ready:
        raise RuntimeError(reason)

    work.mkdir(parents=True, exist_ok=True)
    script_file = work / 'narration_script.txt'
    script_file.write_text(script.strip(), encoding='utf-8')
    audio = work / 'narration.wav'
    subs = work / 'words.srt'
    worker = root / 'tools' / 'kokoro_worker.py'
    command([
        str(interpreter_path(root)), str(worker),
        '--model', str(root / 'models' / MODEL.name),
        '--voices-file', str(root / 'models' / VOICES_FILE.name),
        '--script-file', str(script_file), '--voice', voice_id,
        '--speed', str(speed), '--output', str(audio),
    ], cwd=work)
    if not audio.is_file() or audio.stat().st_size < 1024:
        raise RuntimeError('Kokoro failed to generate usable audio')
    length = duration(audio)
    if length > 180:
        raise ValueError('Narration is longer than the three-minute video limit')
    estimated_word_srt(script, length, subs)
    return audio, subs
