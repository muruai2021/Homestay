@echo off
chcp 65001 >nul 2>&1
title create scheduled task
cd /d %~dp0
echo ================================================
echo create daily scrape task (8:00 AM)
echo ================================================
schtasks /create /tn "xinghuoban_daily_scrape" /tr "%~dp0scrape.bat" /sc daily /st 08:00 /f
echo.
echo task created! press any key to exit
pause >nul