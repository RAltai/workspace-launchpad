#!/bin/bash

echo "🔧 Setting up Local Dashboard (Global Python Mode)"

# Step 1: Install dependencies globally
echo "📦 Installing Python packages globally..."
pip3 install --upgrade pip --break-system-packages
pip3 install playwright pyyaml --break-system-packages

# Step 2: Install Playwright browsers
echo "🧭 Installing Playwright browser support..."
playwright install

# Step 3: Create LaunchAgent for macOS auto-start
PLIST_PATH="$HOME/Library/LaunchAgents/local.dashboard.plist"
PROJECT_DIR="$(cd "$(dirname "$0")"; pwd)"

echo "📄 Writing LaunchAgent to $PLIST_PATH"

cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>local.dashboard</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$PROJECT_DIR/server.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>WorkingDirectory</key>
  <string>$PROJECT_DIR</string>
  <key>StandardOutPath</key>
  <string>$PROJECT_DIR/out.log</string>
  <key>StandardErrorPath</key>
  <string>$PROJECT_DIR/err.log</string>
</dict>
</plist>
EOF

chmod 644 "$PLIST_PATH"

# Step 4: Load the LaunchAgent
echo "🚀 Loading LaunchAgent..."
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "✅ Setup complete!"
echo "➡️ Dashboard will run on login and be available at: http://localhost:8888"
echo "🧭 Don't forget to set Chrome's new tab to: http://localhost:8888 (via New Tab Redirect extension)"