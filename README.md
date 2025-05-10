# Workspace Launchpad

A **self-hosted, offline bookmark dashboard** built with Flask and YAML. Switch between **Work** and **Personal** modes instantly, with category-based organization, favicon previews, dark/light themes, and persistent storage—**all local**.

---

## 🚀 Features

| Feature                    | Description                                                                 |
| -------------------------- | --------------------------------------------------------------------------- |
| 🔖 Category bookmarks       | Organize bookmarks under custom categories, auto-fetching favicons.         |
| 🌗 Dark / Light theme      | One-click toggle with persistent preference (via localStorage).             |
| 💼🏠 Work & Personal modes | Two isolated YAML files (`work.yaml` and `personal.yaml`) for clean context |
| 🧠 Cache-free interface    | Always displays the freshest data — no browser caching.                     |
| 🧩 New-tab ready           | Can be set as your browser's homepage or new-tab page.                      |
| 📦 Docker support         | Production-ready container using Gunicorn and gthread worker.               |
| 🛠️ Local YAML storage     | All bookmarks stored in readable YAML under `src/data/`                     |
| 🛠️ Import / Export config | Speed up your setup by importing your own YAML configs from the web UI. |

---

## 🧪 Quick Start (Local Dev)

```bash
# Clone the repo
$ git clone https://github.com/RAltai/workspace-launchpad.git
$ cd workspace-launchpad

# Set up virtual environment
$ python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python dependencies
$ pip install -r requirements.txt

# Install browser for favicon snapshots (optional)
$ python -m playwright install chromium

# Run the development server
$ python src/launchpad/app.py
```

Open [http://localhost:8888](http://localhost:8888) in your browser.

---

## 🐳 Docker (Production)

```bash
# Build the image
$ docker build -t workspace-launchpad .

# Run the container
$ docker run -d -p 80:8888 workspace-launchpad
```

By default, the container runs:

```sh
gunicorn -k gthread -w 2 -b 0.0.0.0:8888 app:app
```

---

## 📁 Project Structure

```
workspace-launchpad/
├── src/
│   ├── assets/
│   │   ├── favicons/
│   │   ├── script.js
│   │   └── style.css
│   ├── data/
│   │   ├── work.yaml
│   │   └── personal.yaml
│   ├── templates/
│   │   └── index.html
│   └── app.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

---

## ✍️ Example Bookmarks (YAML)

### `src/data/work.yaml`

```yaml
Dashboards:
  - title: GitHub
    url: https://github.com
    favicon: /assets/favicons/github.com.ico
Tools:
  - title: Jenkins
    url: https://jenkins.io
    favicon: /assets/favicons/jenkins.io.ico
```

### `src/data/personal.yaml`

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

---

## 🧰 Customization

| File                      | Purpose                         |
| ------------------------- | ------------------------------- |
| `src/launchpad/frontend/` | Frontend assets: JS, CSS, icons |
| `src/launchpad/config.py` | Custom environment toggles      |
| `src/launchpad/views.py`  | Flask route logic               |
| `src/data/*.yaml`         | User bookmark data              |

---

## 🌐 Browser Integration

* **Firefox:** Use [New Tab Override](https://addons.mozilla.org/en-US/firefox/addon/new-tab-override/) to point your new tab to `http://localhost:8888`
* **Chrome/Edge:** Use [New Tab Redirect](https://chrome.google.com/webstore/detail/new-tab-redirect/icpgjfneehieebagbmdbhnlpiopdcmna)

---

## 📄 License

MIT
