@echo off
REM start.bat - One-click starter for Windows
SETLOCAL
if not exist venv\Scripts\activate (
  echo Creating virtual environment...
  python -m venv venv
  call venv\Scripts\activate
  echo Installing dependencies...
  pip install -r requirements.txt
) else (
  call venv\Scripts\activate
)
python app.py
PAUSE
