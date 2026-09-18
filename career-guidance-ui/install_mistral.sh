#!/bin/bash
# Mistral LLM Installation Script for Linux/Mac
# This script installs dependencies and optionally downloads the Mistral model

echo "============================================================"
echo "Mistral LLM Installation for Career Guidance Chatbot"
echo "============================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Step 1: Installing Python dependencies..."
echo ""
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 2: Model Setup"
echo "============================================================"
echo ""
echo "You have three options:"
echo ""
echo "1. Automated setup (downloads model automatically)"
echo "2. Manual setup (you download the model yourself)"
echo "3. Skip model setup (use fallback AI only)"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Running automated setup..."
        python3 setup_mistral.py
        ;;
    2)
        echo ""
        echo "Manual Setup Instructions:"
        echo ""
        echo "1. Visit: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
        echo "2. Download: mistral-7b-instruct-v0.2.Q4_K_M.gguf (4.4 GB)"
        echo "3. Create folder: backend/models"
        echo "4. Move the downloaded file to: backend/models/"
        echo "5. Add to .env file: MISTRAL_MODEL_PATH=backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        echo ""
        read -p "Press Enter to continue..."
        ;;
    3)
        echo ""
        echo "Skipping model setup. The chatbot will use fallback AI."
        echo "This still works great - just without LLM enhancement."
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "Step 3: Testing Installation"
echo "============================================================"
echo ""
python3 test_mistral_integration.py
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some tests failed, but the system should still work."
    echo "The chatbot will use fallback AI if Mistral is unavailable."
else
    echo ""
    echo "SUCCESS: All tests passed!"
fi

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Start your Flask server: python3 flask_cors_config.py"
echo "2. Open the app and test the chatbot"
echo "3. Check server logs for model status"
echo ""
echo "For more information, see:"
echo "- MISTRAL_QUICKSTART.md (quick start guide)"
echo "- MISTRAL_INTEGRATION_GUIDE.md (detailed documentation)"
echo ""
