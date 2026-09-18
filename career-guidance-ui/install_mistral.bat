@echo off
REM Mistral LLM Installation Script for Windows
REM This script installs dependencies and optionally downloads the Mistral model

echo ============================================================
echo Mistral LLM Installation for Career Guidance Chatbot
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
echo.
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 2: Model Setup
echo ============================================================
echo.
echo You have two options:
echo.
echo 1. Automated setup (downloads model automatically)
echo 2. Manual setup (you download the model yourself)
echo 3. Skip model setup (use fallback AI only)
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Running automated setup...
    python setup_mistral.py
) else if "%choice%"=="2" (
    echo.
    echo Manual Setup Instructions:
    echo.
    echo 1. Visit: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF
    echo 2. Download: mistral-7b-instruct-v0.2.Q4_K_M.gguf (4.4 GB)
    echo 3. Create folder: backend\models
    echo 4. Move the downloaded file to: backend\models\
    echo 5. Add to .env file: MISTRAL_MODEL_PATH=backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    echo Skipping model setup. The chatbot will use fallback AI.
    echo This still works great - just without LLM enhancement.
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 3: Testing Installation
echo ============================================================
echo.
python test_mistral_integration.py
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed, but the system should still work.
    echo The chatbot will use fallback AI if Mistral is unavailable.
) else (
    echo.
    echo SUCCESS: All tests passed!
)

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Start your Flask server: python flask_cors_config.py
echo 2. Open the app and test the chatbot
echo 3. Check server logs for model status
echo.
echo For more information, see:
echo - MISTRAL_QUICKSTART.md (quick start guide)
echo - MISTRAL_INTEGRATION_GUIDE.md (detailed documentation)
echo.
pause
