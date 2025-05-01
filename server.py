
import http.server
import socketserver
import os
import json
import urllib.parse
import yaml
from pathlib import Path
from urllib.request import urlopen, Request
from playwright.sync_api import sync_playwright

PORT = 8888
DATA_FILE = "data.yaml"
FAVICON_DIR = "favicons"
THUMBNAIL_DIR = "thumbnails"
Path(FAVICON_DIR).mkdir(exist_ok=True)
Path(THUMBNAIL_DIR).mkdir(exist_ok=True)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'Chats': [], 'Dashboards': [], 'Docs': [], 'Tools': [] }
    with open(DATA_FILE, 'r') as f:
        return yaml.safe_load(f) or {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        yaml.dump(data, f)

def get_favicon(domain):
    try:
        favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
        local_path = f"{FAVICON_DIR}/{domain}.ico"
        req = Request(favicon_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response, open(local_path, 'wb') as out_file:
            out_file.write(response.read())
        return f"/{local_path}"
    except:
        parts = domain.split('.')
        if len(parts) > 2:
            fallback_domain = '.'.join(parts[-2:])
            return get_favicon(fallback_domain)
        else:
            return "/default.ico"

def take_thumbnail(url, name):
    path = f"{THUMBNAIL_DIR}/{name}.png"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=30000)
            page.screenshot(path=path, full_page=False)
            browser.close()
        return f"/{path}"
    except Exception as e:
        return "/default.png"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/fetch_favicon"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            url = query.get("url", [""])[0]
            domain = urllib.parse.urlparse(url).netloc

            try:
                favicon_path = get_favicon(domain)
                thumbnail_path = take_thumbnail(url, domain.replace('.', '_'))
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "favicon": favicon_path,
                    "thumbnail": thumbnail_path
                }).encode())
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "favicon": "/default.ico",
                    "thumbnail": "/default.png"
                }).encode())
        else:
            super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        data = json.loads(self.rfile.read(length))
        db = load_data()

        if self.path == "/add":
            entry = {
                "title": data.get("title", ""),
                "url": data.get("url", ""),
                "favicon": data.get("favicon", "/default.ico")
            }
            db[data["category"]].append(entry)
            save_data(db)
            self.send_response(200)
            self.end_headers()

        elif self.path == "/remove":
            db[data["category"]].pop(data["index"])
            save_data(db)
            self.send_response(200)
            self.end_headers()

        elif self.path == "/update":
            cat, idx, field, val = data["category"], data["index"], data["field"], data["value"]
            db[cat][idx][field] = val
            save_data(db)
            self.send_response(200)
            self.end_headers()

os.chdir(os.path.dirname(__file__))
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    httpd.serve_forever()
