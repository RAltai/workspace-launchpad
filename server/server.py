from flask import Flask, send_from_directory, render_template, jsonify, request
import yaml, os, pathlib

app = Flask(__name__, static_folder=str(pathlib.Path(__file__).resolve().parent.parent / "assets"), template_folder=str(pathlib.Path(__file__).resolve().parent.parent / "templates"))
DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"

def load_data(mode):
    with open(DATA_DIR / f"{mode}.yaml") as f:
        return yaml.safe_load(f) or {}

@app.route("/")
def index():
    mode = request.args.get("mode", "work")
    return render_template("index.html", mode=mode)

@app.route("/data/<mode>.yaml")
def data_yaml(mode):
    return send_from_directory(DATA_DIR, f"{mode}.yaml")

@app.after_request
def add_no_cache_headers(resp):
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

if __name__ == "__main__":
    app.run(port=8888)