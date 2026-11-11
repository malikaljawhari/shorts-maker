"""Lightweight tests; avoid downloading a 140MB voice model in CI."""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

import natural_voice
from natural_voice import KOKORO_VOICES, interpreter_path, make_kokoro_voice, voice_ready


def test_has_multiple_natural_voices():
    assert len(KOKORO_VOICES) >= 8
    assert 'am_michael' in KOKORO_VOICES.values()
    assert 'bf_emma' in KOKORO_VOICES.values()


def test_missing_models_explained(tmp_path):
    ok, reason = voice_ready(tmp_path)
    assert not ok
    assert 'model' in reason.lower()


def test_model_files_no_venv_python314(tmp_path, monkeypatch):
    models = tmp_path / 'models'
    models.mkdir()
    (models / 'kokoro-v1.0.int8.onnx').write_bytes(b'0' * 1_000_005)
    (models / 'voices-v1.0.bin').write_bytes(b'0' * 1_000_005)
    with patch.object(natural_voice.sys, 'version_info', (3, 14, 8)):
        # The actual interpreter may be 3.13; mock ensures the compatibility gate.
        with patch('natural_voice.interpreter_path', return_value=Path(sys.executable)):
            ok, reason = voice_ready(tmp_path)
            assert not ok and '3.14' in reason


def test_natural_voice_validates_input_before_model_check(tmp_path):
    for name, speed, text in [('invalid', 1.0, 'hello there'), ('am_michael', 1.4, 'hello there'), ('am_michael', 1.0, '')]:
        with pytest.raises(ValueError):
            make_kokoro_voice(text, name, speed, tmp_path, root=tmp_path)


def test_interpreter_path_returns_current_when_no_sidecar(tmp_path):
    assert interpreter_path(tmp_path) == Path(sys.executable)


def test_worker_logic_calls_create(tmp_path, monkeypatch):
    # The voice worker is dependency-injected with dummy modules, so CI does not need the model.
    import importlib.util
    from types import SimpleNamespace
    worker_path = Path(natural_voice.__file__).parent / 'tools' / 'kokoro_worker.py'
    spec = importlib.util.spec_from_file_location('kokoro_worker', worker_path)
    worker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(worker)
    calls = {}
    class FakeKokoro:
        def __init__(self, model, voices):
            calls['model'] = model
        def create(self, script, voice, speed, lang):
            calls['params'] = (script, voice, speed, lang)
            return [0.0] * 200, 24000
    def fake_write(path, samples, rate, subtype):
        calls['write'] = (path, rate, subtype)
    monkeypatch.setitem(sys.modules, 'kokoro_onnx', SimpleNamespace(Kokoro=FakeKokoro))
    monkeypatch.setitem(sys.modules, 'soundfile', SimpleNamespace(write=fake_write))
    worker.synthesize(tmp_path/'m.onnx', tmp_path/'v.bin', 'Hello there', 'bm_george', .95, tmp_path/'voice.wav')
    assert calls['params'] == ('Hello there', 'bm_george', .95, 'en-gb')
    assert calls['write'][2] == 'PCM_16'
