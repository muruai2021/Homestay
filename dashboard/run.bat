@echo off
chcp 65001 >nul 2>&1
title xinghuoban
cd /d %~dp0
echo ================================================
echo xinghuoban dashboard - auto start
echo ================================================
echo.
echo [1/2] starting local server...
start /min cmd /c "cd /d %~dp0 && node server.js"
timeout /t 3 /nobreak >nul
echo [2/2] opening browser...
start http://127.0.0.1:3000/dashboard-v2.html
echo.
echo ================================================
echo done! do not close this window
echo press any key to exit
echo ================================================
pause >nul