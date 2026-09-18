# How to Use Progress Tracking

## Visual Guide

### Progress Tracking Tab Layout

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Track Your Progress                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Overall Completion: 25.5%                                   │
│  [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]        │
│                                                              │
│  Current Week: [  2  ]                                       │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 🕐 Python                           75%  [ Save ]     │  │
│  │    ~60h estimated                                     │  │
│  │    [████████████████████░░░░░░░░░░░░░░░░░░░░░░░░]    │  │
│  │    0%          50%          100%                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 🕐 React                            50%  [ Save ]     │  │
│  │    ~50h estimated                                     │  │
│  │    [████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]    │  │
│  │    0%          50%          100%                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 🕐 Docker                            0%  [ Save ]     │  │
│  │    ~30h estimated                                     │  │
│  │    [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]    │  │
│  │    0%          50%          100%                      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Step-by-Step Instructions

### Step 1: Go to Progress Tracking Tab
Click on "Progress Tracking" in the tab menu (between "Chat With AI" and "Evolution Over Time")

### Step 2: Find the Skill You Want to Update
You'll see a list of all skills from your routine. Each skill shows:
- Skill name (e.g., "Python")
- Estimated hours (e.g., "~60h estimated")
- Current completion percentage (e.g., "75%")
- A slider bar
- A **"Save" button** (orange/yellow color)

### Step 3: Move the Slider
- Click and drag the slider to set your completion percentage
- The slider moves in 5% increments (0%, 5%, 10%, 15%, etc.)
- The percentage number updates as you move the slider

### Step 4: Click the "Save" Button
- **IMPORTANT**: After moving the slider, you MUST click the "Save" button
- The "Save" button is located to the right of the percentage number
- It's an orange/yellow button with white text
- When clicked, it will show "Saving..." briefly
- After saving, it returns to "Save"

### Step 5: Repeat for Other Skills
- Update and save progress for 2-3 skills minimum
- This gives you enough data to see evolution metrics

### Step 6: View Evolution
- Go to "Evolution Over Time" tab
- The data should auto-load
- Or click "Load Evolution Data" button
- You'll now see your progress metrics!

## Button Location

The "Save" button is here:

```
┌─────────────────────────────────────────────────────┐
│ 🕐 Python                    75%  [ Save ] ← HERE! │
│    ~60h estimated                                   │
│    [████████████████████░░░░░░░░░░░░░░░░░░░░░░]    │
└─────────────────────────────────────────────────────┘
```

## Button Appearance

- **Color**: Orange/yellow background with orange border
- **Text**: "Save" (or "Saving..." when clicked)
- **Size**: Small rectangular button
- **Location**: Right side of each skill card, next to the percentage

## What Happens When You Click Save

1. Button text changes to "Saving..."
2. Backend receives the progress update
3. Progress is stored in the system
4. Button returns to "Save"
5. Overall completion percentage updates at the top

## Troubleshooting

### "I don't see the Save button"

**Check**:
- Are you on the "Progress Tracking" tab?
- Have you generated a routine first?
- Is the routine loaded? (You should see skill cards)

**If still not visible**:
- Try refreshing the page (Ctrl+R or Cmd+R)
- Check browser zoom level (should be 100%)
- Try a different browser

### "Save button is grayed out"

**Cause**: Button is disabled while saving

**Solution**: Wait a moment for the previous save to complete

### "Nothing happens when I click Save"

**Check**:
1. Is backend running? (`python flask_cors_config.py`)
2. Are you logged in?
3. Check browser console (F12) for errors

## Example Workflow

```
1. Generate Routine
   ↓
2. Go to "Progress Tracking" tab
   ↓
3. Python: Move slider to 75% → Click "Save"
   ↓
4. React: Move slider to 50% → Click "Save"
   ↓
5. Docker: Move slider to 25% → Click "Save"
   ↓
6. Go to "Evolution Over Time" tab
   ↓
7. See your progress metrics! 🎉
```

## Visual Cues

### Before Saving:
- Slider at 0%
- Clock icon (🕐) in orange
- "Save" button in orange

### After Saving:
- Slider at your set percentage
- Overall completion updates
- Ready to view in Evolution tab

### When Complete (100%):
- Green checkmark icon (✓)
- Green border around skill card
- Counts toward "Skills Completed" in Evolution

## Tips

1. **Update regularly**: Track your progress weekly
2. **Be honest**: Set realistic completion percentages
3. **Save often**: Don't forget to click Save after moving slider
4. **Check evolution**: View your growth in Evolution tab
5. **Adjust as needed**: You can update progress multiple times

## Common Mistakes

❌ Moving slider but not clicking Save
✅ Move slider AND click Save

❌ Expecting auto-save
✅ Manual save required (click button)

❌ Updating all skills to 100% immediately
✅ Update realistically as you learn

## Need Help?

If you still can't find the Save button:
1. Take a screenshot of your Progress Tracking tab
2. Check if you see skill cards with sliders
3. Look for orange/yellow buttons on the right side
4. Verify you're logged in and have a routine generated

---

**Remember**: Move slider → Click "Save" button → Progress is saved! 🚀
