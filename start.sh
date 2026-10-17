#!/bin/bash
cd "$(dirname "$0")"
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
else
  echo "Creating virtualenv..."
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi
python app.py
