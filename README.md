# A-Level Past Papers (Flask)

This repository contains a small Flask app (MVP) for uploading, previewing, downloading, and searching A-level mathematics past papers. The site uses English UI and supports pairing mark schemes with question papers.

Use the branch `feature/alevel-pastpapers` for the current implementation.

Use the website: https://Yvounne.github.io/alevel-pastpapers  
(If you want the live site deployed via GitHub Pages, I can add a deployment step next.)

Quick start (local):

1. Clone the repo and switch to the branch:
   git clone https://github.com/Yvounne/alevel-pastpapers.git
   cd alevel-pastpapers
   git checkout feature/alevel-pastpapers

2. Create a virtualenv and install requirements:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Run the app:
   ./start.sh

4. Open http://127.0.0.1:5000

Notes:
- Uploads are stored in `uploads/` organized by module slug.
- Max upload size is 50 MB and only PDF files are allowed.
- When uploading a mark scheme you can optionally pair it with an existing question paper in the same module.
