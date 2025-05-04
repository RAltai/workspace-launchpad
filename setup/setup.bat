@echo off
cd /d %~dp0\..
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium

REM --- Add to startup ----------------------------------
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
echo @echo off > "%STARTUP%\workspace-launchpad.bat"
echo cd /d %~dp0 >> "%STARTUP%\workspace-launchpad.bat"
echo call venv\Scripts\activate>>"%STARTUP%\workspace-launchpad.bat"
echo python server\server.py>>"%STARTUP%\workspace-launchpad.bat"
echo ✓ Added launch script to Windows Startup folder

REM --- Optional: enforce Chrome new‑tab policy ----------
set /p CHPOL=Configure Chrome/Edge new-tab automatically? (y/N):
if /i "%CHPOL%"=="Y" (
  reg add "HKCU\Software\Policies\Google\Chrome" /v NewTabPageLocation /t REG_SZ /d http://localhost:8888 /f
  reg add "HKCU\Software\Policies\Microsoft\Edge" /v NewTabPageLocation /t REG_SZ /d http://localhost:8888 /f
  echo ✓ Policy created (browser may show "managed by your organization").
) else (
  echo • Please install "New Tab Redirect" extension manually.
)
echo Done. Open http://localhost:8888 in your browser!
