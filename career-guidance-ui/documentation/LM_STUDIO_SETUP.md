# LM Studio Setup Guide

## Quick Setup (5 Minutes)

### Step 1: Open LM Studio
- Launch LM Studio on your PC

### Step 2: Download/Load Mistral Model
1. Click on the **Search** tab (🔍)
2. Search for: **"Mistral 7B Instruct"**
3. Download one of these (recommended):
   - `mistralai/Mistral-7B-Instruct-v0.2` (Q4_K_M) - **Best balance**
   - `mistralai/Mistral-7B-Instruct-v0.2` (Q5_K_M) - Higher quality
   - `mistralai/Mistral-7B-Instruct-v0.2` (Q3_K_M) - Faster, smaller

### Step 3: Load the Model
1. Go to **Chat** tab (💬)
2. Click **"Select a model to load"**
3. Choose the Mistral model you downloaded
4. Wait for it to load (shows "Model loaded" when ready)

### Step 4: Start Local Server
1. Click on **Local Server** tab (🌐) or the server icon
2. Click **"Start Server"**
3. Default URL: `http://localhost:1234/v1`
4. Keep LM Studio running!

### Step 5: Configure Your App (Optional)
If LM Studio uses a different port, add to `.env`:
```env
LM_STUDIO_URL=http://localhost:YOUR_PORT/v1
```

### Step 6: Test It
```bash
cd career-guidance-ui/backend
python test_mistral_integration.py
```

You should see:
```
✅ LM Studio connected successfully!
   Using model: mistralai/Mistral-7B-Instruct-v0.2
```

### Step 7: Start Your Flask Server
```bash
cd ..
python flask_cors_config.py
```

Look for:
```
✅ LM Studio connected successfully!
```

## That's It!

Your chatbot now uses LM Studio for faster, better responses!

---

## Troubleshooting

### "LM Studio not running or not accessible"
**Solution**: 
1. Make sure LM Studio is open
2. Make sure a model is loaded
3. Make sure the server is started (green indicator)

### "LM Studio is running but no model loaded"
**Solution**: 
1. Go to Chat tab in LM Studio
2. Load a Mistral model
3. Restart your Flask server

### Different Port?
If LM Studio uses a different port (not 1234):
1. Check the port in LM Studio's Local Server tab
2. Add to `.env`: `LM_STUDIO_URL=http://localhost:YOUR_PORT/v1`

---

## Advantages of LM Studio

✅ **Faster**: Optimized inference engine
✅ **Better GPU Support**: Automatic GPU acceleration
✅ **Easy Model Management**: GUI for downloading/switching models
✅ **Lower Memory**: Better memory optimization
✅ **Real-time Monitoring**: See token generation in real-time

---

## Fallback System

If LM Studio is not running, the system automatically:
1. Tries to use llama-cpp-python (if model file exists)
2. Falls back to rule-based AI (always works!)

**No errors, no crashes** - the chatbot always works!

---

## Performance Comparison

| Method | Speed | GPU Support | Setup |
|--------|-------|-------------|-------|
| LM Studio | ⚡⚡⚡ Fastest | ✅ Automatic | Easy |
| llama-cpp-python | ⚡⚡ Fast | ⚠️ Manual | Medium |
| Fallback | ⚡ Instant | N/A | None |

---

## Recommended Settings in LM Studio

### For Best Performance:
- **GPU Offload**: Max (if you have GPU)
- **Context Length**: 2048
- **Temperature**: 0.7
- **Max Tokens**: 512

### For Lower Memory:
- Use Q4_K_M or Q3_K_M quantization
- Reduce GPU offload layers
- Lower context length to 1024

---

## Keep LM Studio Running

For the chatbot to use LM Studio:
- ✅ LM Studio must be open
- ✅ A model must be loaded
- ✅ Local server must be started

If you close LM Studio, the system automatically falls back to rule-based AI.

---

**Enjoy faster, smarter responses with LM Studio!** 🚀
