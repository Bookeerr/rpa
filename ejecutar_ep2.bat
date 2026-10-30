@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 exit /b 1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_ep2.ps1" %*
exit /b %errorlevel%
