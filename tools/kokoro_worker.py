"""Invoke Kokoro in its own compatible Python 3.12 interpreter. No network calls."""
from __future__ import annotations

import argparse
from pathlib import Path


def synthesize(model: Path, voices_file: Path, script: str, voice: str,
               speed: float, output: Path) -> None:
    from kokoro_onnx import Kokoro
    import soundfile as sf

    synth = Kokoro(str(model), str(voices_file))
    samples, sample_rate = synth.create(
        script, voice=voice, speed=speed,
        lang='en-gb' if voice.startswith(('bf_', 'bm_')) else 'en-us',
    )
    if samples is None or len(samples) == 0:
        raise RuntimeError('Kokoro produced no audio')
    output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output), samples, sample_rate, subtype='PCM_16')


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate an offline Kokoro WAV voiceover')
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--voices-file', type=Path, required=True)
    parser.add_argument('--script-file', type=Path, required=True)
    parser.add_argument('--voice', required=True)
    parser.add_argument('--speed', type=float, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    script = args.script_file.read_text(encoding='utf-8')
    if not script.strip() or len(script) > 5000 or not (0.80 <= args.speed <= 1.20):
        parser.error('Invalid script or speed')
    synthesize(args.model, args.voices_file, script, args.voice, args.speed, args.output)
    print('Kokoro WAV created successfully')


if __name__ == '__main__':
    main()
