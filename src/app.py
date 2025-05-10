from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import urllib.parse
import urllib.request

import yaml
from flask import Flask, jsonify, render_template, request, send_file, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSET_DIR = BASE_DIR / "assets"
FAV_DIR = ASSET_DIR / "favicons"
THUMB_DIR = ASSET_DIR / "thumbnails"

ALLOWED_MODES = {"work", "personal"}
DEFAULT_FAVICON = "/assets/favicons/default.ico"

for path in (FAV_DIR, THUMB_DIR):
    path.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=str(ASSET_DIR), template_folder=str(BASE_DIR / "templates"))

def yaml_path(mode: str) -> Path:
    return DATA_DIR / f"{mode}.yaml"

def load_yaml(mode: str) -> Dict[str, List[Dict[str, str]]]:
    path = yaml_path(mode)
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}

def save_yaml(mode: str, data: Dict[str, Any]) -> None:
    with yaml_path(mode).open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False)

def google_favicon(domain: str, *, size: int = 64) -> str:
    return f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"

def ensure_favicon(url: str) -> str:
    domain = urllib.parse.urlparse(url).hostname or "default"
    ico_file = FAV_DIR / f"{domain}.ico"

    if not ico_file.exists():
        try:
            with urllib.request.urlopen(google_favicon(domain)) as resp:
                ico_file.write_bytes(resp.read())
        except Exception:
            return DEFAULT_FAVICON

    return str(ico_file.relative_to(BASE_DIR))

def validated_mode(mode: str) -> str:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"Invalid mode {mode!r}")
    return mode

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data/<mode>.yaml")
def data_yaml(mode: str):
    try:
        validated_mode(mode)
    except ValueError:
        return jsonify(error="Invalid mode"), 400

    return send_from_directory(DATA_DIR, f"{mode}.yaml")

@app.post("/add")
def add_link():
    b = request.get_json(force=True) or {}
    mode, cat = b.get("mode"), b.get("category")
    if not (mode and cat):
        return jsonify(error="Missing mode or category"), 400

    data = load_yaml(mode)
    data.setdefault(cat, [])

    data[cat].append(
        {
            "title": b["title"],
            "url": b["url"],
            "favicon": ensure_favicon(b["url"]),
        }
    )
    save_yaml(mode, data)
    return jsonify(status="ok")

@app.post("/update")
def update_link():
    b = request.get_json(force=True) or {}
    mode, cat = b.get("mode"), b.get("category")
    if not (mode and cat):
        return jsonify(error="Missing mode or category"), 400

    data = load_yaml(mode)
    for link in data.get(cat, []):
        if link["title"] == b["orig_title"]:
            link.update(title=b["title"], url=b["url"], favicon=ensure_favicon(b["url"]))
            break
    else:
        return jsonify(error="Link not found"), 404

    save_yaml(mode, data)
    return jsonify(status="ok")

@app.post("/remove")
def remove_link():
    b = request.get_json(force=True) or {}
    mode, cat = b.get("mode"), b.get("category")
    if not (mode and cat):
        return jsonify(error="Missing mode or category"), 400

    data = load_yaml(mode)
    data[cat] = [l for l in data.get(cat, []) if l["title"] != b["title"]]
    save_yaml(mode, data)
    return jsonify(status="ok")

@app.post("/add_category")
def add_category():
    b = request.get_json(force=True) or {}
    mode = b.get("mode")
    cat = (b.get("category") or "").strip()

    if not cat:
        return jsonify(error="Empty category"), 400

    data = load_yaml(mode)
    if cat in data:
        return jsonify(error="Category exists"), 409

    data[cat] = []
    save_yaml(mode, data)
    return jsonify(status="ok")

@app.post("/delete_category")
def delete_category():
    b = request.get_json(force=True) or {}
    mode, cat = b.get("mode"), b.get("category")

    data = load_yaml(mode)
    if cat in data:
        data.pop(cat)
        save_yaml(mode, data)

    app.logger.info("Deleted category %s from %s", cat, mode)
    return jsonify(status="ok")

@app.post("/import_yaml")
def import_yaml():
    mode = request.args.get("mode", "")
    if mode not in ALLOWED_MODES:
        return jsonify(error="Invalid mode"), 400

    uploaded = request.files.get("file")
    if uploaded is None:
        return jsonify(error="No file uploaded"), 400
    if not uploaded.filename.endswith(".yaml"):
        return jsonify(error="Invalid file type"), 400

    try:
        data = yaml.safe_load(uploaded.read().decode("utf-8")) or {}
    except Exception as exc:  # noqa: BLE001
        return jsonify(error=f"Invalid YAML: {exc}"), 400

    save_yaml(mode, data)
    return jsonify(status="ok")

@app.get("/export_yaml")
def export_yaml():
    mode = request.args.get("mode", "")
    if mode not in ALLOWED_MODES:
        return jsonify(error="Invalid mode"), 400

    path = yaml_path(mode)
    if not path.exists():
        return jsonify(error=f"{mode}.yaml not found"), 404

    return send_file(
        path,
        as_attachment=True,
        download_name=f"{mode}.yaml",
        mimetype="text/yaml",
    )

@app.post("/move_link")
def move_link():
    b = request.get_json(force=True) or {}
    mode = b.get("mode")
    from_cat, to_cat = b.get("from_category"), b.get("to_category")
    old_index, new_index = b.get("old_index"), b.get("new_index")

    bookmarks = load_yaml(mode)
    try:
        item = bookmarks[from_cat].pop(old_index)
    except (IndexError, KeyError, TypeError):
        return jsonify(success=False, error="Invalid source index or category"), 400

    bookmarks.setdefault(to_cat, []).insert(new_index, item)
    if not bookmarks[from_cat]:
        del bookmarks[from_cat]

    save_yaml(mode, bookmarks)
    return jsonify(success=True)

@app.after_request
def disable_cache(resp):
    resp.headers.update(
        {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
    )
    return resp

if __name__ == "__main__":
    app.run("0.0.0.0", port=8888)
