# PDF/DOCX Upload Fix

## Issue
When uploading PDF or DOCX files, the "Generate Routine" button remained disabled.

## Root Cause
The button's `disabled` attribute was checking for `analyzeData` state:
```jsx
disabled={!analyzeData || isGenerating}
```

However, `analyzeData` is only set when parsing JSON files. For PDF and DOCX files, only `uploadedFile` was being set, leaving `analyzeData` as `null`.

## Solution
Changed the button condition to check for `uploadedFile` instead:

### Before:
```jsx
<button
    onClick={handleGenerateRoutine}
    disabled={!analyzeData || isGenerating}
    className={`... ${analyzeData && !isGenerating ? '...' : '...'}`}
>
```

### After:
```jsx
<button
    onClick={handleGenerateRoutine}
    disabled={!uploadedFile || isGenerating}
    className={`... ${uploadedFile && !isGenerating ? '...' : '...'}`}
>
```

## Files Modified
- `career-guidance-ui/src/pages/RoutineBuild.jsx`
  - Line 281: Changed `disabled={!analyzeData || isGenerating}` to `disabled={!uploadedFile || isGenerating}`
  - Line 282: Changed `${analyzeData && !isGenerating` to `${uploadedFile && !isGenerating`
  - Removed unused `buildRoutine` import

## Testing
1. Upload a PDF file → Button should now be enabled ✅
2. Upload a DOCX file → Button should now be enabled ✅
3. Upload a JSON file → Button should still work ✅

## How It Works Now

### File Upload Flow:
1. User uploads file (JSON, PDF, or DOCX)
2. `uploadedFile` state is set for all file types
3. `analyzeData` state is only set for JSON (for preview purposes)
4. Button checks `uploadedFile` (not `analyzeData`)
5. Button is enabled for all file types ✅

### Generate Routine Flow:
1. User clicks "Generate Routine"
2. `handleGenerateRoutine()` checks `uploadedFile`
3. Calls `generateRoutineFromFile(uploadedFile, 10)`
4. Backend processes the file (JSON, PDF, or DOCX)
5. Returns routine data
6. UI displays the routine

## Visual Feedback
When a file is uploaded, the UI shows:
- File name in cyan color
- "Click to replace" message
- Upload icon changes to indicate success

## Status
✅ Fixed and tested
✅ No diagnostics errors
✅ All file types now work correctly
