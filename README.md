# Workspace Launchpad – Local Bookmark Dashboard

Workspace Launchpad is an **offline**, Flask‑powered new‑tab page that lets you keep two independent bookmark sets (Work + Personal), switchable with one click, and a persistent dark/light theme. All data is stored in YAML on your own machine.

## Key Features
- 🔖 Organise bookmarks by category, with fetched favicons.
- 🌗 One‑click dark/light toggle (saved in `localStorage`).
- 💼🏠 Work / Personal mode toggle (each has its own YAML).
- 🔄 No browser‑side caching — you always see the latest bookmarks.
- 🚀 Can be your browser’s New‑Tab / Start Page (via extension or policy).
- 🖥 macOS, Linux, Windows setup scripts; Python 3.9+.

## Quick Start
```bash
git clone <repo> workspace-launchpad
cd workspace-launchpad
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
python server/server.py
````

Open [http://localhost:8888](http://localhost:8888).

Run `setup/setup.sh` (macOS/Linux) or `setup/setup.bat` (Windows) for automatic venv creation, dependency install, login‑start integration, and guided browser configuration.

See full usage, customisation, and troubleshooting at the end of this file.

````

*(Add any extra instructions you need.)*

---

## 4. Directory `data/` – YAML files

### `data/work.yaml`

```yaml
Dashboards:
  - title: GitHub
    url: https://github.com
    favicon: /assets/favicons/github.com.ico
Tools:
  - title: Jenkins
    url: https://jenkins.io
    favicon: /assets/favicons/jenkins.io.ico
````

### `data/personal.yaml`

```yaml
Media:
  - title: YouTube
    url: https://youtube.com
    favicon: /assets/favicons/youtube.com.ico
Shopping:
  - title: Amazon
    url: https://amazon.com
    favicon: /assets/favicons/amazon.com.ico
```

*(Feel free to edit or add categories/links — every top‑level key is a category.)*

---

## Docker setup

```
docker build -t workspace-page .
docker run -d -p 80:8888 workspace-page
```
