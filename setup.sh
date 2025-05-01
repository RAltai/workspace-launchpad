#!/bin/bash

echo "🔧 Setting up local dashboard..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
playwright install

# Install New Tab Redirect if Chrome is open
echo "⚠️ Please make sure you have the Chrome extension 'New Tab Redirect' installed."
echo "➡️ Set your new tab page to: http://localhost:8888"

# Setup login item (macOS only)
LOGIN_SCRIPT="$HOME/Library/LaunchAgents/local.dashboard.plist"

cat <<EOF > "$LOGIN_SCRIPT"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>local.dashboard</string>
  <key>ProgramArguments</key>
  <array>
    <string>${PWD}/venv/bin/python3</string>
    <string>${PWD}/server.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>WorkingDirectory</key>
  <string>${PWD}</string>
  <key>StandardOutPath</key>
  <string>${PWD}/out.log</string>
  <key>StandardErrorPath</key>
  <string>${PWD}/err.log</string>
</dict>
</plist>
EOF

launchctl load "$LOGIN_SCRIPT"

echo "✅ Setup complete. The dashboard will auto-start on login."