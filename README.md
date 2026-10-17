# A-Level Past Papers (Flask)

This repository holds a cleaned branch ready for a replacement A-Level past papers web app. The main branch now contains the run instructions and placeholder notes — further development will be done on `main` unless you ask otherwise.

This README explains how to open and run the website locally from the repository and where to look for a live site if deployed.

---

## Quick summary

- Active branch for development: `main` (per your request)
- Current state: placeholder "cleaned" files in the repo. Replace the app code in this branch to run the full site.
- Default local URL (when running the Flask dev server): `http://127.0.0.1:5000`

---

## Run the website locally (recommended for development)

1. Clone the repository and switch to the main branch:

   ```bash
   git clone https://github.com/Yvounne/alevel-pastpapers.git
   cd alevel-pastpapers
   git checkout main
   ```

2. Create and activate a Python virtual environment (macOS / Linux):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows (PowerShell):

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application (development mode):

   ```bash
   ./start.sh
   ```

   If the script is not executable, run directly:

   ```bash
   python app.py
   ```

5. Open your browser and go to:

   ```text
   http://127.0.0.1:5000
   ```

   You should see the placeholder page if the branch has not yet been replaced with the full app. Once the full app is added, the same URL will serve the full site locally.

---

## Notes about the current (placeholder) repo

- The repository currently contains a minimal placeholder app that prints a message indicating the branch is cleaned. Replace the placeholder files with the full app code (templates, static assets, `app.py`, database schema) to restore the upload/preview/download functionality.
- Uploads (when implemented) will be stored in an `uploads/` directory inside the repository root.
- The expected Flask server address is `127.0.0.1:5000` unless you change the `app.run()` host/port or run behind a different WSGI server.

---

## Deploying / Live site

- If you want a publicly accessible site, we can deploy to a server (VPS) or add a GitHub Actions workflow to deploy to a hosting provider. GitHub Pages supports static sites only — for a Flask app you will need a server/container-based host or convert to a static frontend.

---

## What I can do next for you (on `main`)

- Replace the placeholder code with your corrected app code and push it to `main`.
- Add a GitHub Actions workflow to build and deploy the app (to a VM/container host or to a hosting provider).
- Set up a Dockerfile and a docker-compose configuration for easy local and remote deployment.
- Help configure Gunicorn + Nginx and provide example systemd service files.

If you want me to update the `main` branch now with your replacement code, paste the code here and say "Replace main with this code" and I will push it and (optionally) open a PR.
