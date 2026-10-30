@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\..\scripts\open_studio.ps1" -Robot MAIN_TESTFIRE_EP2
exit /b %errorlevel%
