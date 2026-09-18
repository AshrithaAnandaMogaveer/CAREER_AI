# Mistral Local LLM Integration Guide

## Overview

The career guidance chatbot now supports local Mistral LLM integration for more dynamic and intelligent responses. The system automatically falls back to rule-based responses if the model is unavailable, ensuring zero disruption to existing features.

## Features

✅ **Local LLM Integration**: Run Mistral-7B model locally for intelligent responses
✅ **Automatic Fallback**: Seamlessly falls back to rule-based AI if model unavailable
✅ **Context-Aware**: Uses routine and progress data for personalized responses
✅ **Zero Breaking Changes**: Existing features continue to work without modification
✅ **Easy Setup**: Simple installation and configuration process

## Architecture

```
User Question
     ↓
Flask Endpoint (/api/routine-chat)
     ↓
MistralLocalChat
     ↓
  ┌─────────────────┐
  │ Mistral Model   │ → Dynamic LLM Response
  │   Available?    │
  └─────────────────┘
     ↓ (if not available)
RoutineChatAI (Fallback)
     ↓
Rule-Based Response
```

## Installation

### Step 1: Install Dependencies

```bash
cd career-guidance-ui/backend
pip install -r requirements.txt
```

This installs `llama-cpp-python` which enables local LLM inference.

### Step 2: Download Mistral Model

#### Option A: Automated Setup (Recommended)

```bash
python setup_mistral.py
```

This script will:
1. Verify llama-cpp-python installation
2. Show available Mistral models
3. Download your selected model
4. Configure the .env file automatically

#### Option B: Manual Setup

1. Download a Mistral GGUF model from HuggingFace:
   - **Recommended**: [Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
   - Choose Q4_K_M quantization for best balance (~4.4 GB)

2. Create models directory:
   ```bash
   mkdir backend/models
   ```

3. Place the downloaded `.gguf` file in `backend/models/`

4. Update `.env` file:
   ```env
   MISTRAL_MODEL_PATH=backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
   ```

### Step 3: Restart Flask Server

```bash
python flask_cors_config.py
```

The server will automatically detect and load the Mistral model.

## Model Recommendations

| Model | Size | Quality | Speed | Use Case |
|-------|------|---------|-------|----------|
| Q3_K_M | ~3.5 GB | Good | Fast | Limited resources |
| Q4_K_M | ~4.4 GB | Better | Balanced | **Recommended** |
| Q5_K_M | ~5.3 GB | Best | Slower | High quality needed |

## Configuration

### Environment Variables

Add to `.env` file:

```env
# Mistral Local LLM Configuration
MISTRAL_MODEL_PATH=backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

### Model Parameters

Edit `mistral_local_chat.py` to adjust:

```python
self.llm = Llama(
    model_path=self.model_path,
    n_ctx=2048,        # Context window size
    n_threads=4,       # CPU threads (adjust based on your CPU)
    n_gpu_layers=0,    # Set to 35 for full GPU offload (requires CUDA)
    verbose=False
)
```

### GPU Acceleration (Optional)

For faster inference with NVIDIA GPU:

1. Install CUDA-enabled version:
   ```bash
   CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
   ```

2. Update `n_gpu_layers` in `mistral_local_chat.py`:
   ```python
   n_gpu_layers=35  # Offload all layers to GPU
   ```

## Testing

### Test Mistral Integration

```bash
cd backend
python mistral_local_chat.py
```

Expected output:
```
Testing Mistral Local Chat Integration...

Model Info: {
  "using_mistral": true,
  "model_path": "backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
  "model_loaded": true,
  "fallback_available": true
}

Test 1: General career guidance question
Success: True
Source: mistral_local
...
```

### Test via API

```bash
curl -X POST http://localhost:5000/api/routine-chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userQuestion": "How can I improve my Python skills?",
    "routineData": {},
    "progressData": {}
  }'
```

## How It Works

### 1. Request Flow

```python
# Flask endpoint receives request
@app.route('/api/routine-chat', methods=['POST'])
@token_required
def routine_chat(current_user):
    # Get Mistral chat instance (singleton)
    chat_ai = get_mistral_chat()
    
    # Generate response (automatic fallback)
    result = chat_ai.generate_response(
        user_question,
        routine_data,
        progress_data
    )
```

### 2. Response Generation

```python
# MistralLocalChat checks model availability
if self.use_mistral and self.llm:
    # Use Mistral LLM
    response = self._generate_mistral_response(...)
else:
    # Fallback to rule-based AI
    response = self.fallback_ai.generate_response(...)
```

### 3. Context Building

The system builds context-aware prompts:

```
System Context: You are an expert Career Guidance AI Mentor...

User Context:
- Learning routine: 12 weeks, 15 hours/week
- Total skills to learn: 8
- Progress: 35% complete
- Skills completed: 3

User Question: How should I organize my study schedule?

Response: [Mistral generates contextual advice]
```

## Fallback Behavior

The system automatically falls back to rule-based responses when:

- Mistral model is not configured
- Model file is not found
- llama-cpp-python is not installed
- Model loading fails
- Generation encounters an error

**No user-facing errors occur** - the chatbot continues to work seamlessly.

## Response Format

Both Mistral and fallback AI return the same format:

```json
{
  "success": true,
  "response": "Here's how to improve your Python skills...",
  "action_items": [
    "Practice coding daily",
    "Build small projects",
    "Join Python communities"
  ],
  "category": "skill_specific",
  "timestamp": "2026-03-07T10:30:00",
  "source": "mistral_local"  // or "fallback"
}
```

## Performance

### Expected Response Times

| Configuration | Response Time |
|--------------|---------------|
| CPU (4 threads, Q4_K_M) | 3-8 seconds |
| CPU (8 threads, Q4_K_M) | 2-5 seconds |
| GPU (CUDA, Q4_K_M) | 1-2 seconds |
| Fallback (rule-based) | <100ms |

### Memory Usage

| Model | RAM Required |
|-------|--------------|
| Q3_K_M | ~4 GB |
| Q4_K_M | ~6 GB |
| Q5_K_M | ~8 GB |

## Troubleshooting

### Model Not Loading

**Symptom**: Console shows "⚠️ Mistral model not found"

**Solutions**:
1. Verify model file exists at the path in `.env`
2. Check file permissions
3. Ensure path is absolute or relative to backend directory

### llama-cpp-python Import Error

**Symptom**: "⚠️ llama-cpp-python not installed"

**Solution**:
```bash
pip install llama-cpp-python
```

### Slow Response Times

**Solutions**:
1. Increase `n_threads` in model configuration
2. Use smaller quantization (Q3_K_M instead of Q5_K_M)
3. Enable GPU acceleration if available
4. Reduce `max_tokens` in generation parameters

### Out of Memory

**Solutions**:
1. Use smaller quantization (Q3_K_M)
2. Reduce `n_ctx` (context window)
3. Close other applications
4. Use fallback mode (set `MISTRAL_MODEL_PATH` to empty)

## Monitoring

### Check Model Status

```python
from mistral_local_chat import get_mistral_chat

chat = get_mistral_chat()
info = chat.get_model_info()
print(info)
```

Output:
```python
{
    'using_mistral': True,
    'model_path': 'backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf',
    'model_loaded': True,
    'fallback_available': True
}
```

### Server Logs

Watch for these messages on server start:

```
✅ Mistral model loaded successfully!
```

or

```
⚠️ Mistral model not found. Using fallback AI.
```

## Best Practices

1. **Start with Q4_K_M**: Best balance of quality and performance
2. **Monitor Memory**: Ensure sufficient RAM for model + application
3. **Use GPU if Available**: Significantly faster inference
4. **Test Fallback**: Ensure rule-based AI works without model
5. **Cache Model**: Keep model loaded (singleton pattern implemented)
6. **Set Reasonable Timeouts**: LLM responses take longer than rule-based

## Comparison: Mistral vs Rule-Based

| Aspect | Mistral LLM | Rule-Based |
|--------|-------------|------------|
| Response Quality | High, contextual | Good, templated |
| Response Time | 2-8 seconds | <100ms |
| Flexibility | Very flexible | Limited patterns |
| Resource Usage | High (4-8 GB RAM) | Minimal |
| Setup Complexity | Moderate | None |
| Reliability | Requires model | Always available |

## Future Enhancements

Potential improvements:

1. **Model Caching**: Pre-load responses for common questions
2. **Streaming Responses**: Stream tokens as they're generated
3. **Fine-tuning**: Train on career guidance specific data
4. **Multi-model Support**: Support other LLMs (Llama, Phi, etc.)
5. **Response Caching**: Cache responses for identical questions
6. **A/B Testing**: Compare Mistral vs rule-based quality

## Support

For issues or questions:

1. Check console logs for error messages
2. Verify model file integrity
3. Test with `python mistral_local_chat.py`
4. Review this guide's troubleshooting section
5. Ensure all dependencies are installed

## Summary

The Mistral integration enhances the chatbot with intelligent, context-aware responses while maintaining complete backward compatibility. The automatic fallback ensures the system remains robust and reliable even without the LLM model configured.

**Key Benefits**:
- More natural, conversational responses
- Better understanding of complex questions
- Context-aware career guidance
- Zero breaking changes to existing features
- Graceful degradation to rule-based responses
