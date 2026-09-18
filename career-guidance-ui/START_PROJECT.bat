@echo off
title Career Guidance System - Launcher
color 0A

echo ============================================
echo   INTELLIGENT CAREER GUIDANCE SYSTEM
echo ============================================
echo.

:: ── Project path ──────────────────────────────────────────────────────────────
set "PROJECT_DIR=%~dp0"
echo  Project folder: %PROJECT_DIR%
echo.

:: ── Check Python ──────────────────────────────────────────────────────────────
echo [1/4] Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Python not found.
    echo  Please install Python from https://python.org
    pause
    exit /b 1
)
python --version
echo  Python OK.
echo.

:: ── Check Node.js ─────────────────────────────────────────────────────────────
echo [2/4] Checking Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Node.js not found.
    echo  Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
node --version
echo  Node.js OK.
echo.

:: ── Check Flask ───────────────────────────────────────────────────────────────
echo [3/4] Checking Python dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo  Flask not found. Installing...
    python -m pip install flask flask-cors flask-sqlalchemy pyjwt bcrypt requests --user
    python -c "import flask" >nul 2>&1
    if %errorlevel% neq 0 (
        echo  Could not auto-install. Run manually:
        echo    python -m pip install flask flask-cors pyjwt bcrypt
        pause
        exit /b 1
    )
)
echo  Python dependencies OK.
echo.

:: ── Check Node modules ────────────────────────────────────────────────────────
echo [4/4] Checking Node dependencies...
if not exist "%PROJECT_DIR%node_modules\" (
    echo  Running npm install...
    cd /d "%PROJECT_DIR%"
    npm install
    if %errorlevel% neq 0 (
        echo  ERROR: npm install failed.
        pause
        exit /b 1
    )
)
echo  Node dependencies OK.
echo.

:: ── Launch Flask Backend ──────────────────────────────────────────────────────
echo  Starting Flask backend  ^>  http://localhost:5000
start "BACKEND - Flask :5000" cmd /k "color 0B && title BACKEND - Flask :5000 && cd /d "%PROJECT_DIR%" && echo. && echo  Backend: http://localhost:5000 && echo. && python flask_cors_config.py"

timeout /t 4 /nobreak >nul

:: ── Launch React Frontend ─────────────────────────────────────────────────────
:: BROWSER=none is set in .env so React will NOT auto-open the browser.
:: We open it once ourselves below after compilation.
echo  Starting React frontend  ^>  http://localhost:3000
start "FRONTEND - React :3000" cmd /k "color 0E && title FRONTEND - React :3000 && cd /d "%PROJECT_DIR%" && echo. && echo  Frontend: http://localhost:3000 && echo. && npm start"

:: ── Wait for React to compile then open browser exactly ONCE ──────────────────
echo.
echo  Waiting for React to compile (~12 seconds)...
timeout /t 12 /nobreak >nul

echo  Opening browser...
start "" http://localhost:3000

echo.
echo ============================================
echo   RUNNING
echo   Frontend  :  http://localhost:3000
echo   Backend   :  http://localhost:5000
echo.
echo   Close the two server windows to stop.
echo   Or run STOP_PROJECT.bat to stop all.
echo ============================================
echo.
pause
