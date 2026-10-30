@echo off
cd /d "%~dp0"
".venv-ep2\Scripts\python.exe" -m scripts.start_local_services
if errorlevel 1 (pause & exit /b 1)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\open_studio.ps1" -Robot MAIN_TESTFIRE_EP2
if errorlevel 1 pause
