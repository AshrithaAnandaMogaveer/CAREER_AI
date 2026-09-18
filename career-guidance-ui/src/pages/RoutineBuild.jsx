import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Upload, FileText, Zap, BookOpen, MessageCircle,
    BarChart2, TrendingUp, Loader, Send, CheckCircle,
    Clock, Target, Star, Calendar, Lightbulb, AlertCircle
} from 'lucide-react';
import {
    getEvolutionData, generateRoutineFromFile, routineChat, updateRoutineProgress, getRoutineEvolution
} from '../services/routineService';
import SimpleLineChart from '../components/charts/SimpleLineChart';
import SimpleBarChart from '../components/charts/SimpleBarChart';
import SimplePieChart from '../components/charts/SimplePieChart';

// Tab configuration
const TABS = [
    { id: 'routine', label: 'Routine To Follow', icon: BookOpen },
    { id: 'chat', label: 'Chat With AI', icon: MessageCircle },
    { id: 'progress', label: 'Progress Tracking', icon: BarChart2 },
    { id: 'evolution', label: 'Evolution Over Time', icon: TrendingUp },
];

const RoutineBuild = () => {
    // File upload state
    const [uploadedFile, setUploadedFile] = useState(null);
    const [analyzeData, setAnalyzeData] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [fileError, setFileError] = useState('');
    const fileInputRef = useRef(null);

    // Routine state
    const [routine, setRoutine] = useState(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [buildError, setBuildError] = useState('');

    // Tab state
    const [activeTab, setActiveTab] = useState('routine');

    // Chat state
    const [chatMessages, setChatMessages] = useState([]);
    const [chatInput, setChatInput] = useState('');
    const [isChatLoading, setIsChatLoading] = useState(false);
    const chatEndRef = useRef(null);

    // Progress state
    const [skillProgress, setSkillProgress] = useState({});
    const [isSavingProgress, setIsSavingProgress] = useState(false);

    // Evolution state
    const [evolution, setEvolution] = useState(null);
    const [isLoadingEvolution, setIsLoadingEvolution] = useState(false);

    // Current week
    const [currentWeek, setCurrentWeek] = useState(1);

    // Save notification
    const [saveNotification, setSaveNotification] = useState('');
    const [savedSkills, setSavedSkills] = useState({});

    // Scroll chat to bottom
    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatMessages]);

    // Initialize progress when routine loads
    // Use a ref so we only load from backend ONCE (on first routine load),
    // not every time routine state is updated (e.g. after saving progress metrics)
    const progressLoadedRef = React.useRef(false);

    useEffect(() => {
        if (!routine) return;

        // Only load saved progress on the very first routine load
        if (!progressLoadedRef.current) {
            progressLoadedRef.current = true;
            loadSavedProgress();
        }

        // Welcome message — only set once
        setChatMessages(prev => prev.length === 0 ? [{
            role: 'assistant',
            text: `Welcome! Your routine for ${routine.target_domain || 'your domain'} is ready. Ask me anything about your learning path!`,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }] : prev);
    }, [routine]); // eslint-disable-line react-hooks/exhaustive-deps
    
    // Load saved progress — from localStorage (reliable, user-set values)
    const loadSavedProgress = () => {
        if (!routine) return;

        const user = localStorage.getItem('user');
        const userId = user ? JSON.parse(user)?.id || 'default' : 'default';
        const storageKey = `skillProgress_${userId}`;
        const saved = localStorage.getItem(storageKey);

        const init = {};
        (routine.prioritized_skills || []).forEach(s => { init[s.skill] = 0; });

        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                // Merge saved values into init (only for skills in this routine)
                Object.keys(init).forEach(skill => {
                    if (parsed[skill] !== undefined) init[skill] = parsed[skill];
                });
            } catch { /* ignore parse errors */ }
        }

        setSkillProgress(init);
    };

    // Auto-load evolution when switching to evolution tab
    useEffect(() => {
        if (activeTab === 'evolution' && routine) {
            loadEvolution();
        }
    }, [activeTab, routine, skillProgress]); // eslint-disable-line react-hooks/exhaustive-deps

    // File handling
    const parseFile = async (file) => {
        setFileError('');
        if (!file) return;

        const ext = file.name.split('.').pop().toLowerCase();
        if (!['json', 'pdf', 'docx'].includes(ext)) {
            setFileError('Please upload JSON, PDF, or DOCX file from Analyze module.');
            return;
        }

        try {
            // All file types are now supported by backend
            setUploadedFile(file);
            
            // For JSON, we can still parse it for preview
            if (ext === 'json') {
                const text = await file.text();
                const data = JSON.parse(text);
                setAnalyzeData(data);
            }
        } catch {
            setFileError('Could not parse file. Ensure it is valid.');
        }
    };

    const handleFileDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        parseFile(e.dataTransfer.files[0]);
    };

    const handleFileSelect = (e) => {
        parseFile(e.target.files[0]);
    };

    // Generate routine
    const handleGenerateRoutine = async () => {
        if (!uploadedFile) return;
        setIsGenerating(true);
        setBuildError('');

        const result = await generateRoutineFromFile(uploadedFile, 10);

        if (result.success) {
            setRoutine(result.routine);
            setActiveTab('routine'); // Switch to routine tab
        } else {
            setBuildError(result.message || 'Failed to generate routine.');
        }
        setIsGenerating(false);
    };

    // Chat with AI
    const handleChatSend = async () => {
        const msg = chatInput.trim();
        if (!msg || isChatLoading) return;

        const userMsg = {
            role: 'user',
            text: msg,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setChatMessages(prev => [...prev, userMsg]);
        setChatInput('');
        setIsChatLoading(true);

        const progressData = {
            overall_completion: Object.values(skillProgress).reduce((a, b) => a + b, 0) / Object.keys(skillProgress).length || 0,
            skills_completed: Object.values(skillProgress).filter(v => v >= 100).length
        };

        // Use new routine chat endpoint
        const result = await routineChat(msg, routine, progressData);

        setChatMessages(prev => [...prev, {
            role: 'assistant',
            text: result.success ? result.response : 'Sorry, I could not process that. Please try again.',
            action_items: result.action_items || [],
            category: result.category || 'general',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }]);
        setIsChatLoading(false);
    };

    // Update progress
    const handleProgressChange = (skill, value) => {
        setSkillProgress(prev => ({ ...prev, [skill]: Number(value) }));
    };

    const handleSaveProgress = async (skill) => {
        setIsSavingProgress(true);
        const pct = skillProgress[skill] ?? 0;
        const date = new Date().toISOString();

        try {
            const result = await updateRoutineProgress(currentWeek, skill, pct, date, routine);

            if (result.success) {
                // Persist to localStorage so values survive page refresh
                const user = localStorage.getItem('user');
                const userId = user ? JSON.parse(user)?.id || 'default' : 'default';
                const storageKey = `skillProgress_${userId}`;
                const existing = localStorage.getItem(storageKey);
                const current = existing ? JSON.parse(existing) : {};
                current[skill] = pct;
                localStorage.setItem(storageKey, JSON.stringify(current));

                // Update metrics without triggering routine useEffect
                if (result.progress_metrics) {
                    routine.progress_metrics = result.progress_metrics;
                }
                setSaveNotification(`✓ ${skill}: ${pct}% saved`);
                setTimeout(() => setSaveNotification(''), 3000);
                // Show "Saved" on the button briefly
                setSavedSkills(prev => ({ ...prev, [skill]: true }));
                setTimeout(() => setSavedSkills(prev => ({ ...prev, [skill]: false })), 2000);
                setEvolution(null);
            } else {
                setSaveNotification(`✗ Failed to save ${skill}`);
                setTimeout(() => setSaveNotification(''), 3000);
            }
        } catch (error) {
            console.error('Error saving progress:', error);
            setSaveNotification('✗ Save failed. Please try again.');
            setTimeout(() => setSaveNotification(''), 3000);
        }

        setIsSavingProgress(false);
    };

    // Load evolution — build charts directly from skillProgress state
    const loadEvolution = async () => {
        setIsLoadingEvolution(true);

        try {
            const skills = routine?.prioritized_skills || [];
            if (skills.length === 0 || Object.keys(skillProgress).length === 0) {
                setEvolution(null);
                setIsLoadingEvolution(false);
                return;
            }

            // Build skill_completion from current skillProgress
            const skillCompletion = skills.map(s => ({
                skill: s.skill,
                completion_percentage: skillProgress[s.skill] ?? 0,
                status: (skillProgress[s.skill] ?? 0) >= 100 ? 'Achieved'
                      : (skillProgress[s.skill] ?? 0) > 0 ? 'In Progress'
                      : 'Not Started'
            }));

            const overallCompletion = skillCompletion.reduce((sum, s) => sum + s.completion_percentage, 0)
                / (skillCompletion.length || 1);

            const skillsCompleted = skillCompletion.filter(s => s.completion_percentage >= 100).length;

            // Build a simple weekly progress chart from the schedule
            const weeklyProgress = (routine.weekly_schedule || []).slice(0, 12).map(w => {
                const weekSkills = w.skills || [];
                const completed = weekSkills.filter(s => (skillProgress[s.name || s.skill] ?? 0) >= 100).length;
                const remaining = weekSkills.length - completed;
                return {
                    week_number: w.week,
                    completed_topics: completed,
                    remaining_topics: remaining
                };
            });

            // Build a simple monthly progress from skill progress values
            const today = new Date();
            const monthlyProgress = skillCompletion
                .filter(s => s.completion_percentage > 0)
                .slice(0, 6)
                .map((s, i) => ({
                    month_label: new Date(today.getFullYear(), today.getMonth() - (5 - i), 1)
                        .toLocaleString('default', { month: 'short' }),
                    completed_topics: Math.round(s.completion_percentage / 100 * 8),
                    growth_rate: s.completion_percentage
                }));

            // Build daily progress as a simple cumulative line
            const dailyProgress = skillCompletion
                .filter(s => s.completion_percentage > 0)
                .map((s, i) => ({
                    date: s.skill.slice(0, 8),
                    cumulative_topics: skillCompletion
                        .slice(0, i + 1)
                        .reduce((sum, x) => sum + Math.round(x.completion_percentage / 100), 0)
                }));

            const hasData = skillCompletion.some(s => s.completion_percentage > 0);

            if (!hasData) {
                setEvolution(null);
                setIsLoadingEvolution(false);
                return;
            }

            setEvolution({
                overall_completion: Math.round(overallCompletion * 10) / 10,
                skills_completed: skillsCompleted,
                skills_remaining: skills.length - skillsCompleted,
                daily_progress: dailyProgress,
                weekly_progress: weeklyProgress.filter(w => w.completed_topics > 0 || w.remaining_topics > 0),
                monthly_progress: monthlyProgress,
                skill_completion: skillCompletion,
                overall_metrics: {
                    overall_completion_rate: Math.round(overallCompletion * 10) / 10,
                    completed_topics: skillsCompleted,
                    remaining_topics: skills.length - skillsCompleted,
                    current_streak_days: 0
                },
                motivational_message: overallCompletion >= 80
                    ? "Outstanding progress! You're almost there!"
                    : overallCompletion >= 50
                    ? 'Great work! Keep up the momentum!'
                    : "You're on the right track! Stay consistent!",
                motivational_badge: overallCompletion >= 80 ? '🌟' : overallCompletion >= 50 ? '💪' : '🚀',
                motivational_color: overallCompletion >= 80 ? '#00cc66' : overallCompletion >= 50 ? '#00cccc' : '#6b46c1',
                lagging_skills: skillCompletion
                    .filter(s => s.completion_percentage > 0 && s.completion_percentage < 50)
                    .map(s => ({ skill: s.skill, completion: s.completion_percentage }))
                    .slice(0, 3)
            });
        } catch (error) {
            console.error('Error loading evolution:', error);
            setEvolution(null);
        }

        setIsLoadingEvolution(false);
    };

    // Render helper for bold text
    const renderText = (text) => {
        if (!text) return null;
        return text.split('\n').map((line, li, arr) => {
            const parts = line.split(/\*\*(.*?)\*\*/g);
            return (
                <span key={li}>
                    {parts.map((p, pi) => pi % 2 === 1 ? <strong key={pi} className="font-semibold">{p}</strong> : p)}
                    {li < arr.length - 1 && <br />}
                </span>
            );
        });
    };

    return (
        <div className="min-h-screen bg-[#0f0f1a] pt-24 pb-20 px-4 md:px-8">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-8"
                >
                    <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
                        Routine <span className="text-[#00cccc]">Build</span>
                    </h1>
                    <p className="text-gray-400 text-lg max-w-2xl mx-auto">
                        Upload your analysis report and get a personalized learning routine with AI guidance
                    </p>
                </motion.div>

                {/* File Upload Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="bg-[#161625] rounded-xl border border-gray-800 p-6 mb-6"
                >
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-lg bg-[#00cccc]/10 border border-[#00cccc]/30 flex items-center justify-center">
                            <FileText size={20} className="text-[#00cccc]" />
                        </div>
                        <h2 className="text-white font-semibold text-xl">Upload Analysis Report</h2>
                    </div>

                    {/* Drop zone */}
                    <div
                        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                        onDragLeave={() => setIsDragging(false)}
                        onDrop={handleFileDrop}
                        onClick={() => fileInputRef.current?.click()}
                        className={`relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200
                            ${isDragging ? 'border-[#00cccc] bg-[#00cccc]/5' : 'border-gray-700 hover:border-gray-600 hover:bg-white/[0.02]'}`}
                    >
                        <input ref={fileInputRef} type="file" accept=".json,.pdf,.docx" className="hidden" onChange={handleFileSelect} />
                        <Upload size={40} className="mx-auto mb-4 text-gray-500" />
                        {uploadedFile ? (
                            <div>
                                <p className="text-[#00cccc] font-medium text-lg">{uploadedFile.name}</p>
                                <p className="text-gray-500 text-sm mt-2">Click to replace</p>
                            </div>
                        ) : (
                            <div>
                                <p className="text-gray-300 font-medium text-lg">Drag & drop your analysis report here</p>
                                <p className="text-gray-500 text-sm mt-2">or click to browse • Accepts JSON, PDF, or DOCX</p>
                            </div>
                        )}
                    </div>

                    {fileError && (
                        <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-2">
                            <AlertCircle size={18} className="text-red-400" />
                            <p className="text-red-400 text-sm">{fileError}</p>
                        </div>
                    )}

                    {buildError && (
                        <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-2">
                            <AlertCircle size={18} className="text-red-400" />
                            <p className="text-red-400 text-sm">{buildError}</p>
                        </div>
                    )}

                    {/* Generate button */}
                    <button
                        onClick={handleGenerateRoutine}
                        disabled={!uploadedFile || isGenerating}
                        className={`mt-6 w-full py-4 rounded-xl font-semibold text-base transition-all duration-200 flex items-center justify-center gap-3
                            ${uploadedFile && !isGenerating
                                ? 'bg-[#00cccc] text-[#0f0f1a] hover:bg-[#00b5b5] shadow-lg shadow-[#00cccc]/25'
                                : 'bg-gray-700 text-gray-400 cursor-not-allowed'}`}
                    >
                        {isGenerating ? (
                            <><Loader size={20} className="animate-spin" /> Generating Your Routine...</>
                        ) : (
                            <><Zap size={20} /> Generate Routine</>
                        )}
                    </button>
                </motion.div>

                {/* Tabs Section */}
                <AnimatePresence>
                    {routine && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                        >
                            {/* Tab Navigation */}
                            <div className="bg-[#161625] rounded-xl border border-gray-800 p-2 mb-6">
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                                    {TABS.map((tab) => {
                                        const Icon = tab.icon;
                                        const isActive = activeTab === tab.id;
                                        return (
                                            <button
                                                key={tab.id}
                                                onClick={() => setActiveTab(tab.id)}
                                                className={`relative px-4 py-3 rounded-lg font-medium text-sm transition-all duration-200 flex items-center justify-center gap-2
                                                    ${isActive
                                                        ? 'bg-[#00cccc] text-[#0f0f1a] shadow-lg shadow-[#00cccc]/25'
                                                        : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
                                            >
                                                <Icon size={18} />
                                                <span className="hidden md:inline">{tab.label}</span>
                                                <span className="md:hidden">{tab.label.split(' ')[0]}</span>
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>

                            {/* Tab Content */}
                            <div className="bg-[#161625] rounded-xl border border-gray-800 p-6 min-h-[600px]">
                                <AnimatePresence mode="wait">
                                    {/* Routine To Follow Tab */}
                                    {activeTab === 'routine' && (
                                        <motion.div
                                            key="routine"
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            exit={{ opacity: 0, x: 20 }}
                                            transition={{ duration: 0.2 }}
                                        >
                                            <div className="flex items-center gap-3 mb-6">
                                                <BookOpen size={24} className="text-[#00cccc]" />
                                                <h2 className="text-2xl font-bold text-white">Your Learning Routine</h2>
                                            </div>

                                            {/* Summary Cards */}
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                                                {[
                                                    { label: 'Total Weeks', value: routine.projection?.total_weeks ?? 0, icon: Calendar, color: '#00cccc' },
                                                    { label: 'Total Hours', value: routine.projection?.total_hours ?? 0, icon: Clock, color: '#6b46c1' },
                                                    { label: 'Skills', value: routine.projection?.skills_count ?? 0, icon: Star, color: '#f59e0b' },
                                                    { label: 'Target', value: routine.target_domain ?? 'N/A', icon: Target, color: '#00cc66' },
                                                ].map(({ label, value, icon: Icon, color }) => (
                                                    <div key={label} className="bg-[#0f0f1a] rounded-lg p-4 border border-gray-800">
                                                        <Icon size={20} className="mb-2" style={{ color }} />
                                                        <div className="text-white font-bold text-xl mb-1">{value}</div>
                                                        <div className="text-gray-500 text-xs">{label}</div>
                                                    </div>
                                                ))}
                                            </div>

                                            {/* Smart Navigation — Community */}
                                            <div className="bg-[#0f0f1a] border border-[#00cc66]/20 rounded-xl p-4 mb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                                                <div>
                                                    <p className="text-[#00cc66] text-xs font-semibold tracking-widest uppercase mb-0.5">Learn Faster</p>
                                                    <p className="text-white text-sm font-semibold">Join the community to accelerate your learning</p>
                                                    <p className="text-gray-400 text-xs mt-0.5">Connect with peers, share progress, and get help</p>
                                                </div>
                                                <a
                                                    href="/community"
                                                    className="flex-shrink-0 px-4 py-2 bg-[#00cc66] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00b359] transition-colors"
                                                >
                                                    Go to Community →
                                                </a>
                                            </div>

                                            {/* Weekly Schedule */}
                                            <div className="space-y-4">
                                                <h3 className="text-lg font-semibold text-white mb-4">Week-by-Week Schedule</h3>
                                                {(routine.weekly_schedule || []).map((week) => (
                                                    <div key={week.week} className="bg-[#0f0f1a] rounded-lg border border-gray-800 overflow-hidden">
                                                        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-800 bg-gradient-to-r from-[#00cccc]/5 to-transparent">
                                                            <div className="flex items-center gap-3">
                                                                <div className="w-10 h-10 rounded-lg bg-[#00cccc]/20 border border-[#00cccc]/40 flex items-center justify-center">
                                                                    <span className="text-[#00cccc] font-bold">{week.week}</span>
                                                                </div>
                                                                <div>
                                                                    <span className="text-white font-semibold">Week {week.week}</span>
                                                                    <p className="text-gray-500 text-xs">{week.start_date} → {week.end_date}</p>
                                                                </div>
                                                            </div>
                                                            <div className="text-right">
                                                                <div className="text-[#00cccc] font-bold text-lg">{week.total_hours}h</div>
                                                                <div className="text-gray-500 text-xs">Total Time</div>
                                                            </div>
                                                        </div>
                                                        <div className="p-5 space-y-3">
                                                            {week.skills.map((s, si) => (
                                                                <div key={si} className="p-4 bg-[#161625] rounded-lg border border-gray-700 space-y-3">
                                                                    {/* Skill Header */}
                                                                    <div className="flex items-center justify-between">
                                                                        <div className="flex-1">
                                                                            <div className="flex items-center gap-2 mb-1">
                                                                                <span className="text-white font-medium">{s.name || s.skill}</span>
                                                                                <span className={`px-2 py-0.5 rounded-full text-xs font-medium
                                                                                    ${s.status === 'complete' ? 'bg-green-500/20 text-green-400 border border-green-500/40' : 'bg-[#00cccc]/15 text-[#00cccc] border border-[#00cccc]/30'}`}>
                                                                                    {s.status || 'pending'}
                                                                                </span>
                                                                            </div>
                                                                            {/* Dynamic Topic */}
                                                                            {s.topic && (
                                                                                <p className="text-[#00cccc] text-sm font-medium mb-1">
                                                                                    📚 Topic: {s.topic}
                                                                                </p>
                                                                            )}
                                                                            {/* Dynamic Objective */}
                                                                            {s.objective && (
                                                                                <p className="text-gray-400 text-sm">
                                                                                    🎯 {s.objective}
                                                                                </p>
                                                                            )}
                                                                        </div>
                                                                        <div className="text-right ml-4">
                                                                            <div className="text-white font-semibold">{s.hours}h</div>
                                                                            <div className="text-gray-500 text-xs">Allocated</div>
                                                                        </div>
                                                                    </div>
                                                                    
                                                                    {/* YouTube Video Resource */}
                                                                    {s.video_url && (
                                                                        <div className="pt-3 border-t border-gray-700/50">
                                                                            <div className="flex items-start gap-3">
                                                                                <div className="w-8 h-8 rounded-lg bg-red-500/20 border border-red-500/40 flex items-center justify-center shrink-0">
                                                                                    <svg className="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 24 24">
                                                                                        <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                                                                                    </svg>
                                                                                </div>
                                                                                <div className="flex-1 min-w-0">
                                                                                    <p className="text-gray-400 text-xs mb-1">📺 Learning Resource</p>
                                                                                    <a
                                                                                        href={s.video_url}
                                                                                        target="_blank"
                                                                                        rel="noopener noreferrer"
                                                                                        className="text-white hover:text-[#00cccc] text-sm font-medium transition-colors line-clamp-2 block"
                                                                                    >
                                                                                        {s.video_title || 'Watch Tutorial'}
                                                                                    </a>
                                                                                    <p className="text-gray-600 text-xs mt-1">
                                                                                        {s.video_platform || 'YouTube'} • Click to watch
                                                                                    </p>
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    )}
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </motion.div>
                                    )}

                                    {/* Chat With AI Tab */}
                                    {activeTab === 'chat' && (
                                        <motion.div
                                            key="chat"
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            exit={{ opacity: 0, x: 20 }}
                                            transition={{ duration: 0.2 }}
                                            className="flex flex-col h-[600px]"
                                        >
                                            <div className="flex items-center gap-3 mb-6">
                                                <MessageCircle size={24} className="text-[#6b46c1]" />
                                                <h2 className="text-2xl font-bold text-white">Chat With AI Mentor</h2>
                                            </div>

                                            {/* Messages area */}
                                            <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
                                                {chatMessages.map((msg, i) => (
                                                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                                        <div className={`max-w-[85%] rounded-2xl px-5 py-3 text-sm leading-relaxed
                                                            ${msg.role === 'user'
                                                                ? 'bg-[#6b46c1] text-white rounded-br-sm'
                                                                : 'bg-[#0f0f1a] text-gray-200 border border-gray-700 rounded-bl-sm'}`}>
                                                            <div className="mb-2">{renderText(msg.text)}</div>
                                                            {msg.role === 'assistant' && msg.action_items?.length > 0 && (
                                                                <div className="mt-3 pt-3 border-t border-gray-700/50">
                                                                    <p className="text-xs text-gray-500 mb-2 flex items-center gap-1">
                                                                        <Lightbulb size={12} /> Action Items
                                                                    </p>
                                                                    {msg.action_items.map((item, ai) => (
                                                                        <p key={ai} className="text-xs text-gray-400 mt-1 flex items-start gap-2">
                                                                            <CheckCircle size={12} className="text-[#6b46c1] mt-0.5 shrink-0" />
                                                                            {item}
                                                                        </p>
                                                                    ))}
                                                                </div>
                                                            )}
                                                            <div className="text-right mt-2">
                                                                <span className={`text-xs ${msg.role === 'user' ? 'text-purple-300' : 'text-gray-600'}`}>
                                                                    {msg.time}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                                {isChatLoading && (
                                                    <div className="flex justify-start">
                                                        <div className="bg-[#0f0f1a] border border-gray-700 rounded-2xl rounded-bl-sm px-5 py-3">
                                                            <Loader size={18} className="animate-spin text-[#6b46c1]" />
                                                        </div>
                                                    </div>
                                                )}
                                                <div ref={chatEndRef} />
                                            </div>

                                            {/* Quick suggestions */}
                                            <div className="flex flex-wrap gap-2 mb-4">
                                                {['How do I start?', 'Review my progress', 'I feel stuck', 'Study tips'].map(chip => (
                                                    <button
                                                        key={chip}
                                                        onClick={() => setChatInput(chip)}
                                                        className="text-xs px-3 py-1.5 bg-[#0f0f1a] border border-gray-700 rounded-full text-gray-400 hover:text-white hover:border-[#6b46c1] transition-colors"
                                                    >
                                                        {chip}
                                                    </button>
                                                ))}
                                            </div>

                                            {/* Input area */}
                                            <div className="flex gap-3">
                                                <input
                                                    value={chatInput}
                                                    onChange={e => setChatInput(e.target.value)}
                                                    onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleChatSend()}
                                                    placeholder="Ask your AI mentor anything..."
                                                    className="flex-1 bg-[#0f0f1a] border border-gray-700 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-[#6b46c1] transition-colors"
                                                />
                                                <button
                                                    onClick={handleChatSend}
                                                    disabled={!chatInput.trim() || isChatLoading}
                                                    className="bg-[#6b46c1] hover:bg-[#7c3aed] disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-xl px-5 py-3 transition-colors flex items-center gap-2"
                                                >
                                                    <Send size={18} />
                                                </button>
                                            </div>
                                        </motion.div>
                                    )}

                                    {/* Progress Tracking Tab */}
                                    {activeTab === 'progress' && (
                                        <motion.div
                                            key="progress"
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            exit={{ opacity: 0, x: 20 }}
                                            transition={{ duration: 0.2 }}
                                        >
                                            <div className="flex items-center gap-3 mb-6">
                                                <BarChart2 size={24} className="text-[#f59e0b]" />
                                                <h2 className="text-2xl font-bold text-white">Track Your Progress</h2>
                                            </div>

                                            {/* Save notification */}
                                            {saveNotification && (
                                                <div className={`mb-4 px-4 py-3 rounded-lg text-sm font-medium ${
                                                    saveNotification.startsWith('✓')
                                                        ? 'bg-green-500/15 border border-green-500/30 text-green-400'
                                                        : 'bg-red-500/15 border border-red-500/30 text-red-400'
                                                }`}>
                                                    {saveNotification}
                                                </div>
                                            )}

                                            {/* Overall progress */}
                                            <div className="bg-[#0f0f1a] rounded-lg p-5 border border-gray-800 mb-6">
                                                <div className="flex justify-between items-center mb-3">
                                                    <span className="text-gray-400 font-medium">Overall Completion</span>
                                                    <span className="text-white font-bold text-xl">
                                                        {(Object.values(skillProgress).reduce((a, b) => a + b, 0) / Object.keys(skillProgress).length || 0).toFixed(1)}%
                                                    </span>
                                                </div>
                                                <div className="w-full h-4 bg-gray-800 rounded-full overflow-hidden">
                                                    <motion.div
                                                        className="h-full bg-gradient-to-r from-[#00cccc] to-[#00cc66] rounded-full"
                                                        animate={{ width: `${Object.values(skillProgress).reduce((a, b) => a + b, 0) / Object.keys(skillProgress).length || 0}%` }}
                                                        transition={{ duration: 0.6 }}
                                                    />
                                                </div>
                                            </div>

                                            {/* Current week selector */}
                                            <div className="flex items-center gap-3 mb-6">
                                                <label className="text-gray-400 font-medium">Current Week:</label>
                                                <input
                                                    type="number"
                                                    min="1"
                                                    max="52"
                                                    value={currentWeek}
                                                    onChange={e => setCurrentWeek(Number(e.target.value))}
                                                    className="w-20 px-3 py-2 bg-[#0f0f1a] border border-gray-700 rounded-lg text-white text-center focus:outline-none focus:border-[#f59e0b] transition-colors"
                                                />
                                            </div>

                                            {/* Skills list */}
                                            <div className="space-y-4">
                                                {(routine.prioritized_skills || []).map((skill) => {
                                                    const pct = skillProgress[skill.skill] ?? 0;
                                                    return (
                                                        <div key={skill.skill} className="bg-[#0f0f1a] rounded-lg p-5 border border-gray-800">
                                                            <div className="flex items-center justify-between mb-4">
                                                                <div className="flex items-center gap-3">
                                                                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center border
                                                                        ${pct >= 100 ? 'bg-green-500/20 border-green-500/40' : 'bg-[#f59e0b]/20 border-[#f59e0b]/40'}`}>
                                                                        {pct >= 100 ? <CheckCircle size={20} className="text-green-400" /> : <Clock size={20} className="text-[#f59e0b]" />}
                                                                    </div>
                                                                    <div>
                                                                        <h3 className="text-white font-semibold">{skill.skill}</h3>
                                                                        <p className="text-gray-500 text-sm">~{skill.estimated_hours}h estimated</p>
                                                                    </div>
                                                                </div>
                                                                <div className="flex items-center gap-3">
                                                                    <span className="text-white font-bold text-lg">{pct}%</span>
                                                                    <button
                                                                        onClick={() => handleSaveProgress(skill.skill)}
                                                                        disabled={isSavingProgress}
                                                                        className={`px-4 py-2 border rounded-lg transition-colors text-sm font-medium disabled:opacity-50 ${
                                                                            savedSkills[skill.skill]
                                                                                ? 'bg-green-500/20 text-green-400 border-green-500/40'
                                                                                : 'bg-[#f59e0b]/15 text-[#f59e0b] border-[#f59e0b]/30 hover:bg-[#f59e0b]/25'
                                                                        }`}
                                                                    >
                                                                        {isSavingProgress ? 'Saving...' : savedSkills[skill.skill] ? 'Saved ✓' : 'Save'}
                                                                    </button>
                                                                </div>
                                                            </div>

                                                            {/* Progress slider */}
                                                            <input
                                                                type="range"
                                                                min="0"
                                                                max="100"
                                                                step="5"
                                                                value={pct}
                                                                onChange={e => handleProgressChange(skill.skill, e.target.value)}
                                                                className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-[#f59e0b]"
                                                                style={{
                                                                    background: `linear-gradient(to right, #f59e0b ${pct}%, #1f2937 ${pct}%)`
                                                                }}
                                                            />

                                                            {/* Progress bar */}
                                                            <div className="mt-3 h-3 bg-gray-800 rounded-full overflow-hidden">
                                                                <motion.div
                                                                    className="h-full rounded-full"
                                                                    style={{
                                                                        background: pct >= 100 ? '#00cc66' : pct >= 50 ? '#f59e0b' : '#ef4444'
                                                                    }}
                                                                    animate={{ width: `${pct}%` }}
                                                                    transition={{ duration: 0.4 }}
                                                                />
                                                            </div>

                                                            <div className="flex justify-between mt-2 text-gray-600 text-xs">
                                                                <span>0%</span>
                                                                <span>50%</span>
                                                                <span>100%</span>
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        </motion.div>
                                    )}

                                    {/* Evolution Over Time Tab */}
                                    {activeTab === 'evolution' && (
                                        <motion.div
                                            key="evolution"
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            exit={{ opacity: 0, x: 20 }}
                                            transition={{ duration: 0.2 }}
                                        >
                                            <div className="flex items-center justify-between mb-6">
                                                <div className="flex items-center gap-3">
                                                    <TrendingUp size={24} className="text-[#00cc66]" />
                                                    <h2 className="text-2xl font-bold text-white">Evolution Over Time</h2>
                                                </div>
                                                <button
                                                    onClick={loadEvolution}
                                                    disabled={isLoadingEvolution}
                                                    className="px-4 py-2 bg-[#00cc66]/15 text-[#00cc66] border border-[#00cc66]/30 rounded-lg hover:bg-[#00cc66]/25 transition-colors flex items-center gap-2 text-sm font-medium disabled:opacity-50"
                                                >
                                                    {isLoadingEvolution ? <Loader size={16} className="animate-spin" /> : <TrendingUp size={16} />}
                                                    {isLoadingEvolution ? 'Loading...' : 'Refresh Data'}
                                                </button>
                                            </div>

                                            {evolution ? (
                                                <div className="space-y-6">
                                                    {/* Success Message */}
                                                    <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                                                        <p className="text-green-400 text-sm flex items-center gap-2">
                                                            <CheckCircle size={16} />
                                                            Evolution data loaded successfully! Showing {evolution.overall_metrics?.completed_topics || 0} completed topics across {evolution.skill_completion?.length || 0} skills.
                                                        </p>
                                                    </div>
                                                    
                                                    {/* Stats Grid */}
                                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                                        {[
                                                            { label: 'Overall', value: `${(evolution.overall_completion ?? 0).toFixed(1)}%`, color: '#00cc66', icon: Target },
                                                            { label: 'Monthly Growth', value: `${(evolution.monthly_growth_rate ?? 0).toFixed(1)}%`, color: '#00cccc', icon: TrendingUp },
                                                            { label: 'Completed', value: evolution.overall_metrics?.completed_topics ?? 0, color: '#6b46c1', icon: CheckCircle },
                                                            { label: 'Remaining', value: evolution.skills_remaining ?? 0, color: '#f59e0b', icon: Clock },
                                                        ].map(({ label, value, color, icon: Icon }) => (
                                                            <div key={label} className="bg-[#0f0f1a] rounded-lg p-4 border border-gray-800 text-center">
                                                                <Icon size={20} className="mx-auto mb-2" style={{ color }} />
                                                                <div className="font-bold text-2xl mb-1" style={{ color }}>{value}</div>
                                                                <div className="text-gray-500 text-xs">{label}</div>
                                                            </div>
                                                        ))}
                                                    </div>

                                                    {/* Daily Progress Chart */}
                                                    {evolution.daily_progress && evolution.daily_progress.length > 0 && (
                                                        <div className="bg-[#0f0f1a] rounded-xl border border-gray-800 p-6">
                                                            <SimpleLineChart
                                                                data={evolution.daily_progress}
                                                                xKey="date"
                                                                yKey="cumulative_topics"
                                                                title="Daily Progress (Cumulative Topics)"
                                                                color="#00cccc"
                                                                height={220}
                                                            />
                                                        </div>
                                                    )}

                                                    {/* Weekly Progress Chart */}
                                                    {evolution.weekly_progress && evolution.weekly_progress.length > 0 && (
                                                        <div className="bg-[#0f0f1a] rounded-xl border border-gray-800 p-6">
                                                            <SimpleBarChart
                                                                data={evolution.weekly_progress.map(w => ({
                                                                    week: w.week_label || `W${w.week_number}`,
                                                                    completed: w.completed_topics,
                                                                    remaining: w.remaining_topics
                                                                }))}
                                                                xKey="week"
                                                                yKeys={['completed', 'remaining']}
                                                                title="Weekly Progress (Completed vs Remaining)"
                                                                colors={['#00cc66', '#ef4444']}
                                                                height={220}
                                                            />
                                                        </div>
                                                    )}

                                                    {/* Monthly Progress Chart */}
                                                    {evolution.monthly_progress && evolution.monthly_progress.length > 0 && (
                                                        <div className="bg-[#0f0f1a] rounded-xl border border-gray-800 p-6">
                                                            <SimpleLineChart
                                                                data={evolution.monthly_progress}
                                                                xKey="month_label"
                                                                yKey="completed_topics"
                                                                title="Monthly Progress (Topics Completed per Month)"
                                                                color="#6b46c1"
                                                                height={220}
                                                            />
                                                        </div>
                                                    )}

                                                    {/* Skill Completion Chart */}
                                                    {evolution.skill_completion && evolution.skill_completion.length > 0 && (
                                                        <div className="bg-[#0f0f1a] rounded-xl border border-gray-800 p-6">
                                                            <SimplePieChart
                                                                data={evolution.skill_completion}
                                                                labelKey="skill"
                                                                valueKey="completion_percentage"
                                                                title="Skill Completion Percentage"
                                                                colors={['#00cccc', '#6b46c1', '#f59e0b', '#00cc66', '#ef4444']}
                                                            />
                                                        </div>
                                                    )}

                                                    {/* Current Streak */}
                                                    {evolution.overall_metrics?.current_streak_days > 0 && (
                                                        <div className="bg-gradient-to-r from-[#00cc66]/10 to-transparent rounded-xl border border-[#00cc66]/30 p-5">
                                                            <div className="flex items-center gap-4">
                                                                <div className="text-4xl">🔥</div>
                                                                <div>
                                                                    <div className="text-[#00cc66] font-bold text-2xl">
                                                                        {evolution.overall_metrics.current_streak_days} Day Streak!
                                                                    </div>
                                                                    <p className="text-gray-400 text-sm">Keep the momentum going!</p>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}

                                                    {/* Motivational Message */}
                                                    {evolution.motivational_message && (
                                                        <div
                                                            className="p-5 rounded-xl border text-center"
                                                            style={{
                                                                background: `${evolution.motivational_color ?? '#00cccc'}15`,
                                                                borderColor: `${evolution.motivational_color ?? '#00cccc'}40`,
                                                            }}
                                                        >
                                                            <div className="text-3xl mb-3">{evolution.motivational_badge}</div>
                                                            <p className="text-lg font-medium" style={{ color: evolution.motivational_color ?? '#00cccc' }}>
                                                                {evolution.motivational_message}
                                                            </p>
                                                        </div>
                                                    )}

                                                    {/* Lagging Skills */}
                                                    {(evolution.lagging_skills || []).length > 0 && (
                                                        <div className="bg-[#0f0f1a] rounded-xl border border-yellow-500/30 p-5">
                                                            <div className="flex items-center gap-2 mb-4">
                                                                <AlertCircle size={20} className="text-yellow-400" />
                                                                <h3 className="text-white font-semibold">Skills Needing Attention</h3>
                                                            </div>
                                                            <div className="space-y-2">
                                                                {evolution.lagging_skills.map(ls => (
                                                                    <div key={ls.skill} className="flex items-center justify-between p-3 bg-[#161625] rounded-lg border border-yellow-500/20">
                                                                        <span className="text-white font-medium">{ls.skill}</span>
                                                                        <span className="text-yellow-400 text-sm font-semibold">{ls.completion}% complete</span>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            ) : (
                                                <div className="text-center py-20">
                                                    <TrendingUp size={64} className="mx-auto mb-4 text-gray-700" />
                                                    <h3 className="text-white text-xl font-semibold mb-2">No Evolution Data Yet</h3>
                                                    <p className="text-gray-500 mb-6">Start tracking your progress to see your growth over time</p>
                                                    <button
                                                        onClick={loadEvolution}
                                                        className="px-6 py-3 bg-[#00cc66] text-[#0f0f1a] rounded-lg hover:bg-[#00b359] transition-colors font-semibold"
                                                    >
                                                        Load Evolution Data
                                                    </button>
                                                </div>
                                            )}
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
};

export default RoutineBuild;
