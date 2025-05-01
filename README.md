# 🧭 Local Dashboard Bookmark Manager

This is a fully-local, customizable dashboard for managing your frequently used dashboards, services, tools, and documents — all in one click. It runs locally and stores data privately using a YAML file, displaying only site icons and titles. This tool is ideal for developers, engineers, and anyone who wants a faster, clutter-free way to access work-related resources.

## ✨ Features

- 🔖 Bookmark manager with favicon and title
- 💾 Stores all data in a local YAML file (`data.yaml`)
- 🧠 No remote dependencies or cloud sync
- 🚀 Clickable icons to open sites in a new tab
- 🔐 100% local: No external tracking or calls
- 🛠️ Easily editable via a browser-based GUI

---

## 🖥️ Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/local-dashboard.git
cd local-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

### 2. Start the dashboard

```bash
python3 server.py
```

Visit: [http://localhost:8888](http://localhost:8888)

---

## 🧰 Auto Setup Script (macOS)

Run the included script to:
- Automatically install dependencies
- Set Chrome’s new tab page to `http://localhost:8888` using the New Tab Redirect extension
- Set up the dashboard to auto-run at login

```bash
chmod +x setup.sh
./setup.sh
```

---

## 📁 Project Structure

```
📦 local-dashboard/
├── data.yaml                # Your bookmarks
├── favicons/                # Cached icons
├── script.js                # Front-end logic
├── style.css                # UI styles
├── index.html               # Dashboard layout
├── server.py                # Python HTTP server
├── requirements.txt         # Python dependencies
├── setup.sh                 # Optional: Auto setup script
└── README.md
```

---

## ✅ Tips

- Add, edit, and delete links using the “⋮” button on each card.
- All icons are fetched from Google’s favicon service and stored locally.
- You can customize categories directly in the YAML structure.

---

## 🔐 Privacy

This app is fully local. No data leaves your machine. You own your bookmarks.

---

## 🛠️ License

MIT License – use freely, contribute improvements!