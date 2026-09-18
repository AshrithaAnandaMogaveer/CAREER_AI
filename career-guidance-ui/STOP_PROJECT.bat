@echo off
title Career Guidance System - Stop
color 0C

echo ============================================
echo   STOPPING CAREER GUIDANCE SYSTEM
echo ============================================
echo.

echo  Stopping Flask backend (port 5000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo  Stopping React frontend (port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo  Stopping Node.js processes...
taskkill /IM node.exe /F >nul 2>&1

echo  Stopping Python Flask processes...
taskkill /IM python.exe /F >nul 2>&1

echo.
echo  All servers stopped.
echo ============================================
pause
