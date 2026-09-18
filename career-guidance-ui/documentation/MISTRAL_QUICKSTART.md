# Mistral LLM Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Quick Setup (Recommended)

```bash
# 1. Install dependencies
cd career-guidance-ui/backend
pip install -r requirements.txt

# 2. Run automated setup
python setup_mistral.py

# 3. Test the integration
python test_mistral_integration.py

# 4. Restart your Flask server
cd ..
python flask_cors_config.py
```

That's it! The chatbot now uses Mistral LLM with automatic fallback.

### Option 2: Manual Setup

```bash
# 1. Install llama-cpp-python
pip install llama-cpp-python

# 2. Download Mistral model (choose one)
# Visit: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF
# Download: mistral-7b-instruct-v0.2.Q4_K_M.gguf (~4.4 GB)

# 3. Create models directory
mkdir backend/models

# 4. Move downloaded model to backend/models/

# 5. Add to .env file
echo "MISTRAL_MODEL_PATH=backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf" >> .env

# 6. Test
python backend/test_mistral_integration.py

# 7. Start server
python flask_cors_config.py
```

## ✅ Verify It's Working

### Check Server Logs

When starting the Flask server, look for:

```
🔄 Loading Mistral model from backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf...
✅ Mistral model loaded successfully!
```

or

```
⚠️ Mistral model not found. Using fallback AI.
```

Both are fine! The system works either way.

### Test via Chat

1. Open the Routine Builder in your app
2. Ask a question like: "How can I improve my Python skills?"
3. You should get a detailed, contextual response

### Check Response Source

The API response includes a `source` field:
- `"source": "mistral_local"` - Using Mistral LLM ✅
- `"source": "fallback"` - Using rule-based AI (still works great!)

## 🎯 What You Get

### With Mistral LLM
- More natural, conversational responses
- Better understanding of complex questions
- Context-aware career guidance
- Personalized advice based on your progress

### With Fallback (No Model)
- Fast, reliable responses
- Template-based guidance
- All features still work
- Zero setup required

## 📊 System Requirements

### Minimum (Fallback Mode)
- No additional requirements
- Works on any system

### Recommended (Mistral LLM)
- RAM: 6 GB free
- Storage: 5 GB for model
- CPU: 4+ cores
- OS: Windows/Linux/Mac

### Optimal (GPU Acceleration)
- NVIDIA GPU with 6+ GB VRAM
- CUDA installed
- Faster responses (1-2 seconds)

## 🔧 Common Issues

### "Model not found"
**Solution**: Check that `MISTRAL_MODEL_PATH` in `.env` points to the correct file.

### "llama-cpp-python not installed"
**Solution**: Run `pip install llama-cpp-python`

### Slow responses
**Solutions**:
- Use Q4_K_M instead of Q5_K_M (smaller model)
- Increase CPU threads in `mistral_local_chat.py`
- Enable GPU acceleration (see full guide)

### Out of memory
**Solutions**:
- Use Q3_K_M model (smaller)
- Close other applications
- Use fallback mode (still works great!)

## 📚 Next Steps

1. **Read Full Guide**: See `MISTRAL_INTEGRATION_GUIDE.md` for detailed documentation
2. **Optimize Performance**: Adjust model parameters for your system
3. **Enable GPU**: Set up CUDA for faster inference
4. **Monitor Usage**: Check logs and response times

## 🆘 Need Help?

1. Run tests: `python backend/test_mistral_integration.py`
2. Check logs when starting Flask server
3. Review `MISTRAL_INTEGRATION_GUIDE.md`
4. The system always falls back gracefully - no errors!

## 💡 Pro Tips

1. **Start with Q4_K_M**: Best balance of quality and speed
2. **Test Fallback**: Works great even without the model
3. **Monitor Memory**: Keep an eye on RAM usage
4. **Use GPU**: Much faster if you have NVIDIA GPU
5. **Cache Model**: Model stays loaded (singleton pattern)

## 🎉 Success!

Your chatbot is now powered by Mistral LLM with intelligent fallback. Enjoy more dynamic and helpful career guidance responses!
