@echo off
setlocal
cd /d "%~dp0"
REM Compatibility entry: Phase 7 evaluation settings; credentials and service addresses come from .env.
uv run --no-sync python scripts/start_v2_flash.py %*
set "START_EXIT=%ERRORLEVEL%"
if not "%START_EXIT%"=="0" (
    echo TicketMind launch failed. Check the messages above and your local .env / services.
    pause
)
exit /b %START_EXIT%
