from flask import Flask, render_template, send_from_directory, request, jsonify
from pathlib import Path
import yaml, urllib.parse, urllib.request, subprocess, os, io, base64

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
ASSET_DIR = BASE / "assets"
FAV_DIR = ASSET_DIR / "favicons"
THUMB_DIR = ASSET_DIR / "thumbnails"
FAV_DIR.mkdir(exist_ok=True, parents=True)
THUMB_DIR.mkdir(exist_ok=True, parents=True)

app = Flask(__name__,
            static_folder=str(ASSET_DIR),
            template_folder=str(BASE / "templates"))

# ---------- helpers -------------------------------------------------
def load_yaml(mode):
    f = DATA_DIR / f"{mode}.yaml"
    if not f.exists():
        return {}
    with open(f, encoding="utf-8") as fp:
        return yaml.safe_load(fp) or {}

def save_yaml(mode, data):
    with open(DATA_DIR / f"{mode}.yaml", "w", encoding="utf-8") as fp:
        yaml.safe_dump(data, fp, allow_unicode=True, sort_keys=False)

def favicon_url(domain, size=64):
    return f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"

def ensure_favicon(url):
    domain = urllib.parse.urlparse(url).hostname or "default"
    ico_path = FAV_DIR / f"{domain}.ico"
    if ico_path.exists():
        return str(ico_path.relative_to(BASE))
    try:
        with urllib.request.urlopen(favicon_url(domain)) as r:
            ico_path.write_bytes(r.read())
            return str(ico_path.relative_to(BASE))
    except Exception:
        return "/assets/favicons/default.ico"

# ---------- routes --------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data/<mode>.yaml")
def data_yaml(mode):
    return send_from_directory(DATA_DIR, f"{mode}.yaml")

# --- CRUD JSON APIs -------------------------------------------------
@app.post("/add")
def add_link():
    body = request.get_json()
    mode, cat = body["mode"], body["category"]
    data = load_yaml(mode)
    data.setdefault(cat, [])
    favicon = ensure_favicon(body["url"])
    data[cat].append({"title": body["title"], "url": body["url"], "favicon": favicon})
    save_yaml(mode, data)
    return {"status": "ok"}

@app.post("/update")
def update_link():
    b = request.get_json()
    mode, cat = b["mode"], b["category"]
    data = load_yaml(mode)
    links = data.get(cat, [])
    for link in links:
        if link["title"] == b["orig_title"]:
            link["title"], link["url"] = b["title"], b["url"]
            link["favicon"] = ensure_favicon(b["url"])
            break
    save_yaml(mode, data)
    return {"status": "ok"}

@app.post("/remove")
def remove_link():
    b = request.get_json()
    mode, cat = b["mode"], b["category"]
    data = load_yaml(mode)
    data[cat] = [l for l in data.get(cat, []) if l["title"] != b["title"]]
    save_yaml(mode, data)
    return {"status": "ok"}

# ---------- No‑cache headers ---------------------------------------
@app.after_request
def add_no_cache(r):
    h = r.headers
    h["Cache-Control"] = "no-cache, no-store, must-revalidate"
    h["Pragma"] = "no-cache"
    h["Expires"] = "0"
    return r

# ---------- main ----------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
