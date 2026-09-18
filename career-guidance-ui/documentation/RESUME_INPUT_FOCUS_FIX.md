# Resume Builder Input Focus Fix

## Problem
When users typed in text fields (skills, certifications, achievements, experience, education, projects), the cursor would jump out after each keystroke, making it impossible to complete typing.

## Root Cause
The `Section` component was defined INSIDE the ResumeForm render function. This caused React to create a brand new Section component on every state change, which unmounted and remounted all child inputs, causing them to lose focus.

## Solution

### Primary Fix: Move Section Component Outside
Moved the `Section` component definition outside the `ResumeForm` component so it's only created once, not on every render.

**Before:**
```jsx
const ResumeForm = ({ resumeData, onDataChange }) => {
  // ... state and handlers ...
  
  const Section = ({ title, sectionKey, children }) => (
    // Component definition inside render
  );
  
  return (/* JSX */);
};
```

**After:**
```jsx
const Section = ({ title, sectionKey, children, expandedSections, toggleSection }) => (
  // Component definition outside, stable across renders
);

const ResumeForm = ({ resumeData, onDataChange }) => {
  // ... state and handlers ...
  return (/* JSX */);
};
```

### Secondary Fix: Stable Keys for Array Items
Changed from using array indices or dynamic values as keys to using stable unique IDs:

- **Before**: Arrays contained strings: `['skill1', 'skill2']`
- **After**: Arrays contain objects with IDs: `[{id: 123, text: 'skill1'}, {id: 456, text: 'skill2'}]`

## Files Modified
1. `career-guidance-ui/src/components/resume/ResumeForm.jsx` - Moved Section component outside, added stable IDs
2. `career-guidance-ui/src/components/resume/ResumePreview.jsx` - Handle both string and object formats
3. `career-guidance-ui/src/utils/atsScorer.js` - Handle both string and object formats

## Why This Works
React's reconciliation algorithm:
1. When a component is defined inside another component's render function, React sees it as a NEW component type on every render
2. React unmounts the old component and mounts the new one
3. This destroys the DOM elements (including focused inputs) and creates new ones
4. The new input elements don't have focus, so the cursor disappears

By defining the component outside, React recognizes it as the SAME component type across renders, so it updates the existing DOM elements instead of replacing them.

## Backward Compatibility
All components handle both formats:
- Old format (strings): `['skill1', 'skill2']`
- New format (objects): `[{id: 123, text: 'skill1'}, {id: 456, text: 'skill2'}]`

## Result
✅ Users can now type continuously in all text fields without losing focus
✅ All inputs maintain cursor position during typing
✅ Section expand/collapse works correctly
✅ No breaking changes to existing functionality
✅ Preview and ATS scoring work correctly with both formats
