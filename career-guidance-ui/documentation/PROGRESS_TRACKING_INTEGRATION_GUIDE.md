# Progress Tracking Integration Guide

## Current Issue

The Progress Tracking tab uses a **slider-based percentage system** for overall skill completion, but the Evolution charts need **individual topic-level completion records** with timestamps.

### Current Flow (Not Working for Evolution):
```
User adjusts slider → Saves skill completion % → No individual topic records
```

### Required Flow (For Evolution Charts):
```
User checks topic checkbox → Saves topic completion with timestamp → Evolution can aggregate by day/week/month
```

## Solution: Two-Track Progress System

### Track 1: Weekly Topic Checkboxes (For Evolution Charts)
Display the actual weekly topics from the routine with checkboxes:

```jsx
Week 1: Python Basics & Syntax
[ ] Completed

Week 2: Data Types & Variables  
[ ] Completed

Week 3: Control Flow
[ ] Completed
```

When user checks a box:
- POST to `/api/routine/progress/weekly`
- Saves: `{skill, week_number, topic, completed: true, completed_at: timestamp}`
- Evolution charts can now aggregate this data

### Track 2: Overall Skill Progress (Current System)
Keep the existing slider for overall skill completion percentage.

## Implementation Steps

### Step 1: Add Weekly Topics Display

In the Progress Tracking tab, after the overall progress bar, add:

```jsx
{/* Weekly Topics Checklist */}
<div className="mt-6">
    <h3 className="text-white font-semibold mb-4">Weekly Topics</h3>
    {routine.weekly_schedule?.map((week) => (
        <div key={week.week} className="mb-4">
            <h4 className="text-gray-400 text-sm mb-2">Week {week.week}</h4>
            {week.skills.map((skillEntry, idx) => (
                <TopicCheckbox
                    key={idx}
                    skill={skillEntry.name}
                    weekNumber={week.week}
                    topic={skillEntry.topic}
                    objective={skillEntry.objective}
                />
            ))}
        </div>
    ))}
</div>
```

### Step 2: Create TopicCheckbox Component

```jsx
const TopicCheckbox = ({ skill, weekNumber, topic, objective }) => {
    const [completed, setCompleted] = useState(false);
    const [loading, setLoading] = useState(false);

    // Load initial state
    useEffect(() => {
        loadCompletionStatus();
    }, []);

    const loadCompletionStatus = async () => {
        // Check if this topic is already marked complete
        const response = await fetch(
            `/api/routine/progress/weekly?skill=${skill}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        const result = await response.json();
        if (result.success) {
            const record = result.progress.find(
                p => p.week_number === weekNumber && p.topic === topic
            );
            if (record) {
                setCompleted(record.completed);
            }
        }
    };

    const handleCheckboxChange = async (e) => {
        const isCompleted = e.target.checked;
        setLoading(true);

        const response = await fetch('/api/routine/progress/weekly', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                skill,
                week_number: weekNumber,
                topic,
                completed: isCompleted
            })
        });

        const result = await response.json();
        if (result.success) {
            setCompleted(isCompleted);
        }
        setLoading(false);
    };

    return (
        <div className="flex items-start gap-3 p-3 bg-[#161625] rounded-lg border border-gray-700 mb-2">
            <input
                type="checkbox"
                checked={completed}
                onChange={handleCheckboxChange}
                disabled={loading}
                className="mt-1 w-4 h-4 rounded border-gray-600 text-[#00cccc] focus:ring-[#00cccc]"
            />
            <div className="flex-1">
                <p className="text-white text-sm font-medium">{topic}</p>
                {objective && (
                    <p className="text-gray-500 text-xs mt-1">{objective}</p>
                )}
            </div>
            {completed && (
                <CheckCircle size={16} className="text-green-400 mt-1" />
            )}
        </div>
    );
};
```

### Step 3: Update handleSaveProgress

Keep the existing slider functionality but also update topic-level records:

```jsx
const handleSaveProgress = async (skill) => {
    setIsSavingProgress(true);
    const pct = skillProgress[skill] ?? 0;
    
    // Calculate how many topics should be marked complete based on percentage
    const skillWeeks = routine.weekly_schedule.filter(w => 
        w.skills.some(s => s.name === skill)
    );
    
    const totalTopics = skillWeeks.length;
    const topicsToComplete = Math.floor((pct / 100) * totalTopics);
    
    // Mark topics as complete up to the percentage
    for (let i = 0; i < topicsToComplete; i++) {
        const week = skillWeeks[i];
        const skillEntry = week.skills.find(s => s.name === skill);
        
        if (skillEntry) {
            await fetch('/api/routine/progress/weekly', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    skill,
                    week_number: week.week,
                    topic: skillEntry.topic,
                    completed: true
                })
            });
        }
    }
    
    setIsSavingProgress(false);
};
```

## Quick Fix: Auto-Create Progress Records

If you want Evolution charts to work immediately without changing the UI, add this to the existing `handleSaveProgress`:

```jsx
const handleSaveProgress = async (skill) => {
    setIsSavingProgress(true);
    const pct = skillProgress[skill] ?? 0;
    const date = new Date().toISOString();
    
    // Existing progress update
    const result = await updateRoutineProgress(currentWeek, skill, pct, date, routine);

    // NEW: Also create topic-level records for Evolution charts
    if (result.success && pct > 0) {
        const skillWeeks = routine.weekly_schedule?.filter(w => 
            w.skills.some(s => (s.name || s.skill) === skill)
        ) || [];
        
        const topicsToComplete = Math.floor((pct / 100) * skillWeeks.length);
        
        for (let i = 0; i < topicsToComplete && i < skillWeeks.length; i++) {
            const week = skillWeeks[i];
            const skillEntry = week.skills.find(s => (s.name || s.skill) === skill);
            
            if (skillEntry && skillEntry.topic) {
                await fetch('/api/routine/progress/weekly', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        skill,
                        week_number: week.week,
                        topic: skillEntry.topic,
                        completed: true
                    })
                });
            }
        }
    }
    
    setIsSavingProgress(false);
};
```

## Testing the Integration

### 1. Test Progress Tracking:
```bash
# In browser console after marking progress:
fetch('/api/routine/progress/weekly', {
    headers: {'Authorization': 'Bearer ' + localStorage.getItem('token')}
})
.then(r => r.json())
.then(d => console.log('Progress records:', d))
```

### 2. Test Evolution Analytics:
```bash
# In browser console:
fetch('/api/routine/evolution/analytics', {
    headers: {'Authorization': 'Bearer ' + localStorage.getItem('token')}
})
.then(r => r.json())
.then(d => console.log('Analytics:', d))
```

### 3. Expected Flow:
1. User adjusts slider to 50% for Python
2. Clicks "Save"
3. Backend creates topic records for first 50% of Python topics
4. User goes to Evolution tab
5. Clicks "Refresh Data"
6. Charts display with data from those topic records

## Summary

The disconnect is:
- **Progress Tracking** saves skill-level percentages
- **Evolution Charts** need topic-level completion records

The solution is to either:
1. Add topic checkboxes to Progress Tracking (recommended)
2. Auto-create topic records when saving skill percentages (quick fix)

Choose option 2 for immediate results, then implement option 1 for better UX.
