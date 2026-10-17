#!/usr/bin/env python3
import os
import sqlite3
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, abort
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATABASE = os.path.join(BASE_DIR, "papers.db")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

CATEGORIES = [
    {"title": "Pure Mathematics", "subtitle": "Core algebra, calculus, and trigonometry.", "modules": [
        {"slug": "pure-math-1", "code": "P1", "name": "Pure Mathematics 1"},
        {"slug": "pure-math-2", "code": "P2", "name": "Pure Mathematics 2"},
        {"slug": "pure-math-3", "code": "P3", "name": "Pure Mathematics 3"},
        {"slug": "pure-math-4", "code": "P4", "name": "Pure Mathematics 4"}]},
    {"title": "Mechanics", "subtitle": "Forces, motion, and modelling.", "modules": [
        {"slug": "mechanics-1", "code": "M1", "name": "Mechanics 1"},
        {"slug": "mechanics-2", "code": "M2", "name": "Mechanics 2"},
        {"slug": "mechanics-3", "code": "M3", "name": "Mechanics 3"}]},
    {"title": "Statistics", "subtitle": "Probability, data, and inference.", "modules": [
        {"slug": "statistics-1", "code": "S1", "name": "Statistics 1"},
        {"slug": "statistics-2", "code": "S2", "name": "Statistics 2"},
        {"slug": "statistics-3", "code": "S3", "name": "Statistics 3"}]},
    {"title": "Further Pure Mathematics", "subtitle": "Extension topics for further maths.", "modules": [
        {"slug": "further-pure-math-1", "code": "FP1", "name": "Further Pure Mathematics 1"},
        {"slug": "further-pure-math-2", "code": "FP2", "name": "Further Pure Mathematics 2"},
        {"slug": "further-pure-math-3", "code": "FP3", "name": "Further Pure Mathematics 3"}]}]

MODULES = [(m["slug"], m["name"]) for cat in CATEGORIES for m in cat["modules"]]
MODULE_MAP = {slug: name for slug, name in MODULES}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("FLASK_SECRET", "change-this-secret")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database helpers

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_slug TEXT NOT NULL,
            title TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            stored_filename TEXT NOT NULL,
            paper_type TEXT NOT NULL,
            year TEXT,
            keywords TEXT,
            pair_id INTEGER,
            uploaded_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows


def execute_db(query, args=()):
    conn = get_db()
    cur = conn.execute(query, args)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_paper_or_404(paper_id):
    paper = query_db("SELECT * FROM papers WHERE id = ?", (paper_id,), one=True)
    if paper is None:
        abort(404)
    return paper


init_db()


@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES)


@app.route("/module/<slug>")
def module_page(slug):
    if slug not in MODULE_MAP:
        abort(404)
    papers = query_db(
        "SELECT * FROM papers WHERE module_slug = ? ORDER BY uploaded_at DESC",
        (slug,),
    )
    return render_template("module.html", modules=MODULES, slug=slug, module_name=MODULE_MAP[slug], papers=papers)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        module_slug = request.form.get("module", "").strip()
        title = request.form.get("title", "").strip()
        paper_type = request.form.get("paper_type", "question").strip()
        year = request.form.get("year", "").strip()
        keywords = request.form.get("keywords", "").strip()
        pair_with = request.form.get("pair_with")
        file = request.files.get("file")

        if module_slug not in MODULE_MAP:
            flash("Please select a valid module.", "error")
            return redirect(url_for("upload"))
        if not title:
            flash("Please enter a title.", "error")
            return redirect(url_for("upload", module=module_slug))
        if not file or file.filename == "":
            flash("Please choose a PDF file.", "error")
            return redirect(url_for("upload", module=module_slug))
        if not allowed_file(file.filename):
            flash("Only PDF files are allowed.", "error")
            return redirect(url_for("upload", module=module_slug))

        original = secure_filename(file.filename) or "paper.pdf"
        if not original.lower().endswith(".pdf"):
            original += ".pdf"

        stored = uuid.uuid4().hex + ".pdf"
        module_dir = os.path.join(app.config["UPLOAD_FOLDER"], module_slug)
        os.makedirs(module_dir, exist_ok=True)
        dest_path = os.path.join(module_dir, stored)
        file.save(dest_path)

        pair_id_val = None
        try:
            if pair_with:
                pair_id_val = int(pair_with)
        except Exception:
            pair_id_val = None

        execute_db(
            "INSERT INTO papers (module_slug, title, original_filename, stored_filename, paper_type, year, keywords, pair_id, uploaded_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (module_slug, title, original, stored, paper_type, year, keywords, pair_id_val, datetime.utcnow().isoformat(timespec="seconds")),
        )

        flash("Paper uploaded successfully.", "success")
        return redirect(url_for("module_page", slug=module_slug))

    # GET
    selected = request.args.get("module", "")
    pair_candidates = []
    if selected and selected in MODULE_MAP:
        pair_candidates = query_db(
            "SELECT id, title FROM papers WHERE module_slug = ? AND paper_type = 'question' ORDER BY uploaded_at DESC LIMIT 50",
            (selected,),
        )
    return render_template("upload.html", modules=MODULES, selected=selected, pair_candidates=pair_candidates)


@app.route("/preview/<int:paper_id>")
def preview(paper_id):
    paper = get_paper_or_404(paper_id)
    module_name = MODULE_MAP.get(paper["module_slug"], paper["module_slug"])
    # Load paired paper (if any)
    pair = None
    if paper["pair_id"]:
        pair = query_db("SELECT id, title FROM papers WHERE id = ?", (paper["pair_id"],), one=True)
    # Also find mark scheme if this is a question paper
    linked_mark = None
    if paper["paper_type"] == "question":
        linked_mark = query_db(
            "SELECT id, title FROM papers WHERE pair_id = ? AND paper_type = 'mark'",
            (paper["id"],),
            one=True,
        )
    return render_template("preview.html", paper=paper, module_name=module_name, pair=pair, linked_mark=linked_mark)


@app.route("/file/<int:paper_id>")
def serve_file(paper_id):
    paper = get_paper_or_404(paper_id)
    directory = os.path.join(app.config["UPLOAD_FOLDER"], paper["module_slug"])
    return send_from_directory(directory, paper["stored_filename"], mimetype="application/pdf", as_attachment=False)


@app.route("/download/<int:paper_id>")
def download(paper_id):
    paper = get_paper_or_404(paper_id)
    directory = os.path.join(app.config["UPLOAD_FOLDER"], paper["module_slug"])
    # 'download_name' is available in Flask 2.0+
    return send_from_directory(directory, paper["stored_filename"], as_attachment=True, download_name=paper["original_filename"])


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    module = request.args.get("module", "").strip()
    year = request.args.get("year", "").strip()
    paper_type = request.args.get("paper_type", "").strip()

    clauses = []
    params = []
    if module:
        clauses.append("module_slug = ?")
        params.append(module)
    if year:
        clauses.append("year = ?")
        params.append(year)
    if paper_type:
        clauses.append("paper_type = ?")
        params.append(paper_type)
    if q:
        clauses.append("(title LIKE ? OR original_filename LIKE ? OR keywords LIKE ?)")
        likeq = f"%{q}%"
        params.extend([likeq, likeq, likeq])

    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    sql = f"SELECT * FROM papers {where} ORDER BY uploaded_at DESC LIMIT 200"
    papers = query_db(sql, tuple(params))

    return render_template("search.html", modules=MODULES, papers=papers, query=q, selected_module=module, year=year, paper_type=paper_type)


@app.errorhandler(413)
def too_large(error):
    flash("File too large. Maximum allowed is 50 MB.", "error")
    return redirect(url_for("upload"))


if __name__ == "__main__":
    # Development server
    app.run(host="127.0.0.1", port=5000, debug=True)
