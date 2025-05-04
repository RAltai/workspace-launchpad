#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

echo "▶ Creating Python venv"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

echo "▶ Creating login‑startup service"
if [[ "$OSTYPE" == "darwin"* ]]; then
  plist=~/Library/LaunchAgents/com.workspace.launchpad.plist
  cat > "$plist" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.workspace.launchpad</string>
  <key>ProgramArguments</key>
  <array><string>${PWD}/venv/bin/python</string><string>${PWD}/server/server.py</string></array>
  <key>RunAtLoad</key><true/>
  <key>WorkingDirectory</key><string>${PWD}</string>
  <key>StandardErrorPath</key><string>${PWD}/launchpad.err</string>
  <key>StandardOutPath</key><string>${PWD}/launchpad.out</string>
</dict></plist>
PL
  launchctl load -w "$plist"
  echo "✓ LaunchAgent installed."
else
  # systemd user service
  mkdir -p ~/.config/systemd/user
  srv=~/.config/systemd/user/workspace-launchpad.service
  cat > "$srv" <<SYS
[Unit]
Description=Workspace Launchpad

[Service]
WorkingDirectory=${PWD}
ExecStart=${PWD}/venv/bin/python ${PWD}/server/server.py
Restart=on-failure

[Install]
WantedBy=default.target
SYS
  systemctl --user enable --now workspace-launchpad
  echo "✓ systemd user service installed."
fi

echo "▶ Browser configuration:"
echo "   • Chrome / Edge → install 'New Tab Redirect' and set http://localhost:8888"
echo "   • Firefox      → install 'Custom New Tab' add‑on and set http://localhost:8888"
echo "Done!"
