@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\enable_lan.ps1"
if errorlevel 1 (pause & exit /b 1)
pause
