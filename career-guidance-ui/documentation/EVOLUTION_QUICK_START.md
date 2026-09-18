# Evolution Feature - Quick Start Guide

## For Frontend Developers

### 1. Mark Topic as Completed (Checkbox)

```javascript
// When user clicks checkbox
const markTopicComplete = async (skill, weekNumber, topic, completed) => {
  const response = await fetch('/api/routine/progress/weekly', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      skill: skill,
      week_number: weekNumber,
      topic: topic,
      completed: completed
    })
  });
  
  const result = await response.json();
  return result.success;
};

// Usage
await markTopicComplete('Machine Learning', 1, 'Linear Regression', true);
```

### 2. Get Evolution Analytics (Charts)

```javascript
// Fetch analytics data
const getAnalytics = async (skill = null) => {
  const url = skill 
    ? `/api/routine/evolution/analytics?skill=${encodeURIComponent(skill)}`
    : '/api/routine/evolution/analytics';
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
  
  const result = await response.json();
  return result.analytics;
};

// Usage
const analytics = await getAnalytics();
// or filter by skill
const pythonAnalytics = await getAnalytics('Python');
```

### 3. Display Charts (Chart.js Example)

```jsx
import { Line, Bar, Pie } from 'react-chartjs-2';

// Daily Progress Line Chart
function DailyChart({ dailyProgress }) {
  const data = {
    labels: dailyProgress.map(d => d.date),
    datasets: [{
      label: 'Topics Completed',
      data: dailyProgress.map(d => d.completed_topics),
      borderColor: 'rgb(75, 192, 192)',
    }]
  };
  return <Line data={data} />;
}

// Weekly Progress Bar Chart
function WeeklyChart({ weeklyProgress }) {
  const data = {
    labels: weeklyProgress.map(w => `Week ${w.week_number}`),
    datasets: [
      {
        label: 'Completed',
        data: weeklyProgress.map(w => w.completed_topics),
        backgroundColor: 'rgba(75, 192, 192, 0.8)',
      },
      {
        label: 'Remaining',
        data: weeklyProgress.map(w => w.remaining_topics),
        backgroundColor: 'rgba(255, 99, 132, 0.8)',
      }
    ]
  };
  return <Bar data={data} options={{ scales: { x: { stacked: true }, y: { stacked: true } } }} />;
}

// Skill Completion Pie Chart
function SkillChart({ skillCompletion }) {
  const data = {
    labels: skillCompletion.map(s => s.skill),
    datasets: [{
      data: skillCompletion.map(s => s.completion_percentage),
      backgroundColor: [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
      ]
    }]
  };
  return <Pie data={data} />;
}
```

### 4. Display Metrics Dashboard

```jsx
function MetricsCards({ overallMetrics }) {
  return (
    <div className="metrics-grid">
      <div className="card">
        <h3>Overall Progress</h3>
        <div className="value">{overallMetrics.overall_completion_rate}%</div>
        <p>{overallMetrics.completed_topics} / {overallMetrics.total_topics}</p>
      </div>
      
      <div className="card">
        <h3>Current Streak</h3>
        <div className="value">{overallMetrics.current_streak_days}</div>
        <p>consecutive days</p>
      </div>
      
      <div className="card">
        <h3>Avg Topics/Week</h3>
        <div className="value">{overallMetrics.avg_topics_per_week}</div>
        <p>productivity rate</p>
      </div>
    </div>
  );
}
```

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/routine/progress/weekly` | GET | Get progress records |
| `/api/routine/progress/weekly` | POST | Mark topic complete/incomplete |
| `/api/routine/progress/summary` | GET | Get completion summary |
| `/api/routine/evolution/analytics` | GET | Get chart data |

## Data Structure Reference

### Analytics Response
```javascript
{
  daily_progress: [
    { date: "2024-03-01", completed_topics: 2, cumulative_topics: 2 }
  ],
  weekly_progress: [
    { week_number: 1, completed_topics: 3, remaining_topics: 0, completion_rate: 100.0 }
  ],
  skill_completion: [
    { skill: "Python", total_topics: 10, completed_topics: 8, completion_percentage: 80.0, status: "Achieved" }
  ],
  overall_metrics: {
    total_topics: 18,
    completed_topics: 14,
    remaining_topics: 4,
    overall_completion_rate: 77.8,
    current_streak_days: 5,
    avg_topics_per_week: 2.3,
    estimated_completion_date: "2024-03-15"
  }
}
```

## Testing

```bash
# Backend tests
cd career-guidance-ui/backend
python test_progress_api.py
python test_evolution_analytics.py
```

## Need Help?

- Full docs: `EVOLUTION_ANALYTICS_COMPLETE.md`
- Progress tracking: `PROGRESS_TRACKING_COMPLETE.md`
- Summary: `TASKS_8_9_SUMMARY.md`
