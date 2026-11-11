"""Explicit opt-in model downloader: pinned upstream release assets and SHA-256 checks."""
from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / 'models'
BASE = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/'
ASSETS = {
    'kokoro-v1.0.int8.onnx': 'ae315a79b623f244700e4afb9246c46a26066782e049ba174bf3ba433970ee9c',
    'voices-v1.0.bin': 'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d',
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as file:
        for block in iter(lambda: file.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    MODELS.mkdir(parents=True, exist_ok=True)
    for filename, digest in ASSETS.items():
        target = MODELS / filename
        if target.is_file() and sha256(target).lower() == digest:
            print(f'Already verified: {filename}')
            continue
        temp = MODELS / (filename + '.part')
        print(f'Downloading {filename} from the official Kokoro ONNX GitHub release...')
        try:
            with urllib.request.urlopen(BASE + filename, timeout=45) as response, temp.open('wb') as out:
                while chunk := response.read(1024 * 1024):
                    out.write(chunk)
            if sha256(temp).lower() != digest:
                raise RuntimeError(f'Checksum mismatch for {filename}; delete corrupted file and retry')
            temp.replace(target)
            print(f'Verified: {filename} ({target.stat().st_size // 1_000_000} MB)')
        except Exception:
            temp.unlink(missing_ok=True)
            raise
    print('Kokoro models ready. Nothing was sent to a speech API.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'Model setup failed: {exc}', file=sys.stderr)
        sys.exit(1)
