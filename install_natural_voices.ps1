# Optional setup only. Requires Python 3.12 installed alongside Python 3.14.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
& py -3.12 --version
if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12 first. See docs/NATURAL_VOICES.md' }
& py -3.12 -m venv .voice-venv
if ($LASTEXITCODE -ne 0) { throw 'Voice environment creation failed' }
$voicePython = '.\.voice-venv\Scripts\python.exe'
& $voicePython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'Pip upgrade failed' }
& $voicePython -m pip install -r requirements-voices.txt
if ($LASTEXITCODE -ne 0) { throw 'Voice package installation failed' }
& $voicePython tools\download_kokoro_models.py
if ($LASTEXITCODE -ne 0) { throw 'Voice model download failed' }
Write-Host 'Kokoro is ready. Relaunch Shorts Maker.'
