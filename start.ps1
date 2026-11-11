$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (Test-Path '.venv\Scripts\python.exe') { $python = '.\.venv\Scripts\python.exe' }
elseif (Test-Path '..\.venv\Scripts\python.exe') { $python = '..\.venv\Scripts\python.exe' }
else { throw 'No virtual environment. Read README.md setup section.' }
& $python -m streamlit run app.py
