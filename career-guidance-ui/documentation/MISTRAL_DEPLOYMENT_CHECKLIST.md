# Mistral LLM Integration - Deployment Checklist

## Pre-Deployment Checklist

### ✅ Installation Verification

- [ ] Python 3.8+ is installed
- [ ] All dependencies installed: `pip install -r backend/requirements.txt`
- [ ] llama-cpp-python installed successfully
- [ ] No import errors when running test suite

### ✅ Model Setup (Optional but Recommended)

- [ ] Model downloaded (Q4_K_M recommended)
- [ ] Model placed in `backend/models/` directory
- [ ] `.env` file updated with `MISTRAL_MODEL_PATH`
- [ ] Model file path is correct and accessible
- [ ] Model file is not corrupted (check file size)

### ✅ Testing

- [ ] Run: `python backend/test_mistral_integration.py`
- [ ] All 5 tests pass (5/5)
- [ ] Fallback compatibility verified
- [ ] Mistral integration verified (or fallback working)
- [ ] Response format consistency confirmed
- [ ] Error handling tested
- [ ] No breaking changes detected

### ✅ Configuration

- [ ] `.env` file exists in project root
- [ ] `MISTRAL_MODEL_PATH` set correctly (if using model)
- [ ] File permissions are correct
- [ ] Backend path is accessible
- [ ] No syntax errors in configuration files

### ✅ Code Review

- [ ] `mistral_local_chat.py` - Main integration reviewed
- [ ] `flask_cors_config.py` - Endpoint update reviewed
- [ ] `requirements.txt` - Dependencies verified
- [ ] No merge conflicts
- [ ] All files committed to version control

## Deployment Steps

### Step 1: Backup

- [ ] Backup current working version
- [ ] Backup database (if applicable)
- [ ] Document current configuration
- [ ] Create rollback plan

### Step 2: Install Dependencies

```bash
cd career-guidance-ui/backend
pip install -r requirements.txt
```

- [ ] Installation completed without errors
- [ ] llama-cpp-python version verified

### Step 3: Model Setup (Optional)

**Option A: Automated**
```bash
python backend/setup_mistral.py
```

**Option B: Manual**
- [ ] Download model from HuggingFace
- [ ] Place in `backend/models/`
- [ ] Update `.env` file

**Option C: Skip (Use Fallback)**
- [ ] Confirmed fallback mode works

### Step 4: Run Tests

```bash
python backend/test_mistral_integration.py
```

- [ ] All tests pass
- [ ] No critical errors
- [ ] Warnings reviewed and understood

### Step 5: Start Server

```bash
python flask_cors_config.py
```

- [ ] Server starts without errors
- [ ] Check for model loading message:
  - ✅ "Mistral model loaded successfully!" or
  - ✅ "Mistral model not found. Using fallback AI."
- [ ] No import errors
- [ ] No configuration errors

### Step 6: Functional Testing

- [ ] Open application in browser
- [ ] Navigate to Routine Builder
- [ ] Test chatbot with sample questions:
  - [ ] "How can I improve my Python skills?"
  - [ ] "I'm feeling overwhelmed with learning"
  - [ ] "What's my current progress?"
- [ ] Verify responses are generated
- [ ] Check response quality
- [ ] Verify action items are included

### Step 7: API Testing

```bash
curl -X POST http://localhost:5000/api/routine-chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userQuestion": "How should I organize my study time?",
    "routineData": {},
    "progressData": {}
  }'
```

- [ ] API responds successfully
- [ ] Response format is correct
- [ ] `source` field indicates "mistral_local" or "fallback"
- [ ] No 500 errors

### Step 8: Performance Testing

- [ ] Measure response time (should be 3-8 seconds for Mistral, <100ms for fallback)
- [ ] Check memory usage (should be ~6 GB for Mistral, minimal for fallback)
- [ ] Test with multiple concurrent requests
- [ ] Verify no memory leaks
- [ ] Monitor CPU usage

### Step 9: Error Handling Testing

- [ ] Test with empty question
- [ ] Test with very long question (>1000 chars)
- [ ] Test with invalid tokens
- [ ] Test with missing data
- [ ] Verify graceful error messages

### Step 10: Integration Testing

- [ ] Test with real user accounts
- [ ] Test with actual routine data
- [ ] Test with progress tracking data
- [ ] Verify context-aware responses
- [ ] Test all question categories:
  - [ ] Schedule questions
  - [ ] Improvement questions
  - [ ] Motivation questions
  - [ ] Skill-specific questions
  - [ ] Progress questions

## Post-Deployment Verification

### ✅ Functionality

- [ ] Chatbot responds to all question types
- [ ] Responses are relevant and helpful
- [ ] Action items are generated
- [ ] No error messages to users
- [ ] Fallback works if model unavailable

### ✅ Performance

- [ ] Response times are acceptable
- [ ] Memory usage is stable
- [ ] No performance degradation over time
- [ ] Server remains responsive

### ✅ Monitoring

- [ ] Check server logs for errors
- [ ] Monitor response times
- [ ] Track model usage (Mistral vs fallback)
- [ ] Monitor memory usage
- [ ] Check for any warnings

### ✅ User Experience

- [ ] Users can ask questions easily
- [ ] Responses are displayed correctly
- [ ] No UI breaking changes
- [ ] Mobile responsiveness maintained
- [ ] Loading states work properly

## Rollback Plan

If issues occur:

### Immediate Rollback

1. **Stop the server**
   ```bash
   Ctrl+C or kill process
   ```

2. **Revert Flask endpoint**
   ```python
   # In flask_cors_config.py, change back to:
   from routineChatAI import RoutineChatAI
   chat_ai = RoutineChatAI()
   ```

3. **Restart server**
   ```bash
   python flask_cors_config.py
   ```

4. **Verify functionality**
   - Test chatbot
   - Confirm responses work

### Full Rollback

1. **Restore from backup**
2. **Revert code changes**
3. **Reinstall old dependencies**
4. **Test thoroughly**

## Troubleshooting Guide

### Issue: Model Not Loading

**Symptoms:**
- Warning: "Mistral model not found"
- Using fallback AI

**Solutions:**
- [ ] Check `MISTRAL_MODEL_PATH` in `.env`
- [ ] Verify model file exists
- [ ] Check file permissions
- [ ] Verify file is not corrupted

### Issue: Slow Responses

**Symptoms:**
- Responses take >10 seconds
- High CPU usage

**Solutions:**
- [ ] Use Q4_K_M instead of Q5_K_M
- [ ] Increase `n_threads` in config
- [ ] Enable GPU acceleration
- [ ] Use fallback mode temporarily

### Issue: Out of Memory

**Symptoms:**
- Server crashes
- Memory errors in logs

**Solutions:**
- [ ] Use Q3_K_M model (smaller)
- [ ] Reduce `n_ctx` parameter
- [ ] Close other applications
- [ ] Use fallback mode
- [ ] Add more RAM

### Issue: Import Errors

**Symptoms:**
- "ModuleNotFoundError: llama_cpp"
- Import failures

**Solutions:**
- [ ] Reinstall: `pip install llama-cpp-python`
- [ ] Check Python version (3.8+)
- [ ] Verify virtual environment
- [ ] Check requirements.txt

### Issue: API Errors

**Symptoms:**
- 500 Internal Server Error
- JSON parsing errors

**Solutions:**
- [ ] Check server logs
- [ ] Verify request format
- [ ] Test with curl command
- [ ] Check authentication token

## Monitoring Checklist

### Daily Monitoring

- [ ] Check server logs for errors
- [ ] Monitor response times
- [ ] Check memory usage
- [ ] Verify model is loading correctly

### Weekly Monitoring

- [ ] Review user feedback
- [ ] Analyze response quality
- [ ] Check for any patterns in errors
- [ ] Monitor resource usage trends

### Monthly Monitoring

- [ ] Review overall performance
- [ ] Consider model updates
- [ ] Evaluate user satisfaction
- [ ] Plan optimizations

## Success Criteria

### Minimum Success (Fallback Mode)

- ✅ All tests pass (5/5)
- ✅ Chatbot responds to questions
- ✅ No breaking changes
- ✅ Response time <100ms
- ✅ No user-facing errors

### Optimal Success (Mistral Mode)

- ✅ All tests pass (5/5)
- ✅ Mistral model loads successfully
- ✅ Intelligent, contextual responses
- ✅ Response time 3-8 seconds (CPU) or 1-2 seconds (GPU)
- ✅ No user-facing errors
- ✅ Automatic fallback works

## Documentation Checklist

- [ ] README_MISTRAL.md reviewed
- [ ] MISTRAL_QUICKSTART.md available
- [ ] MISTRAL_INTEGRATION_GUIDE.md complete
- [ ] MISTRAL_ARCHITECTURE.md understood
- [ ] Team trained on new features
- [ ] User documentation updated (if needed)

## Security Checklist

- [ ] No API keys in code
- [ ] Environment variables secured
- [ ] Model files have correct permissions
- [ ] No sensitive data in logs
- [ ] Authentication still working
- [ ] Authorization checks in place

## Final Sign-Off

- [ ] All tests passed
- [ ] Deployment completed successfully
- [ ] Functionality verified
- [ ] Performance acceptable
- [ ] No critical issues
- [ ] Team notified
- [ ] Documentation updated
- [ ] Monitoring in place

**Deployed By:** _______________
**Date:** _______________
**Version:** _______________
**Status:** ✅ Success / ⚠️ Issues / ❌ Rollback

## Notes

_Add any deployment notes, issues encountered, or special configurations here:_

---

## Quick Reference

### Start Server
```bash
python flask_cors_config.py
```

### Run Tests
```bash
python backend/test_mistral_integration.py
```

### Check Model Status
```python
from mistral_local_chat import get_mistral_chat
chat = get_mistral_chat()
print(chat.get_model_info())
```

### View Logs
```bash
# Check server console output
# Look for: "✅ Mistral model loaded" or "⚠️ Using fallback AI"
```

---

**Remember:** The system is designed to always work, even without the Mistral model. Fallback mode is a feature, not a failure!
