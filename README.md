# A-Level Past Papers (Flask)

Easy, one-page guide to open and use the website locally for non-technical users.

This repo currently contains placeholder files. Once the full app is present, the same steps will run the real site.

If you get stuck, copy the exact commands into your terminal (Windows PowerShell, macOS Terminal, or Linux terminal) or follow the one-click options below.

---

## Super-easy ways to open the website (pick one)

Option A — Windows (one double-click)
1. Download the repository ZIP from GitHub or clone it:
   - Download: https://github.com/Yvounne/alevel-pastpapers -> Code -> Download ZIP. Unzip it.
   - Or clone with Git if you know how: `git clone https://github.com/Yvounne/alevel-pastpapers.git`
2. Open the folder and double-click `start.bat`.
3. A terminal window will open and install dependencies (first run) and start the site. When it shows "Running on http://127.0.0.1:5000", open your browser and go to:
   - http://127.0.0.1:5000

Notes: If Windows warns about running a script, choose "Run anyway" or unblock the file in Properties -> General -> Unblock before running.

Option B — macOS / Linux (one terminal command)
1. Download and unzip the repo or clone it:
   - `git clone https://github.com/Yvounne/alevel-pastpapers.git`
   - `cd alevel-pastpapers`
2. Run the start script (these commands will create a virtual environment and start the app):
   - `./start.sh`
3. When the script shows "Running on http://127.0.0.1:5000", open your browser and go to:
   - http://127.0.0.1:5000

Tip: If you see a "Permission denied" when running `./start.sh`, run `chmod +x start.sh` once and try again.

Option C — Docker (one command, advanced but reliable)
- If you have Docker installed, open a terminal in the project folder and run:
  - `docker build -t alevel-pastpapers .`
  - `docker run -p 5000:5000 -v "$(pwd)/uploads:/app/uploads" alevel-pastpapers`
- Open your browser at http://127.0.0.1:5000

---

## Quick troubleshooting (common issues)
- "Command not found" for `python` or `python3`: install Python 3 from https://www.python.org/downloads/
- "pip: command not found": install pip or use the Python installer which includes pip.
- If site doesn't load in browser: check the terminal — the app must say "Running on http://127.0.0.1:5000". If it shows errors, copy them and share them.
- If port 5000 is in use, start with a different port: `python app.py` and edit `app.run(host='127.0.0.1', port=5001)` or run `FLASK_RUN_PORT=5001 python app.py` in some environments.

---

## Quick reference URLs
- Local site: http://127.0.0.1:5000
- Preview endpoint (when app is installed): /preview/<paper_id>
- File serve: /file/<paper_id>
- Download: /download/<paper_id>
- Search: /search?q=term&module=slug&year=YYYY&paper_type=question|mark

---

If you want, I can also:
- Add a short animated GIF showing the steps (I can produce guidance and files, but you must upload images in the repo), or
- Add a Windows installer-like script (PowerShell) that does everything silently.

