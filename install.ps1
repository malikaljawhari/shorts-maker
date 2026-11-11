$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
Write-Host 'Dependencies installed. To launch run: .\start.ps1'
