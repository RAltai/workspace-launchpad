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
