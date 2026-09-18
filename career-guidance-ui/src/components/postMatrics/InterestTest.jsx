import { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, CheckCircle } from 'lucide-react';
import Button from '../Button';

const InterestTest = () => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);
  const [testStarted, setTestStarted] = useState(false);

  const questions = [
    {
      id: 1,
      question: 'I enjoy solving mathematical problems and puzzles',
      cluster: 'analytical',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 2,
      question: 'I like working with my hands and building things',
      cluster: 'technical',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 3,
      question: 'I enjoy helping and teaching others',
      cluster: 'social',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 4,
      question: 'I am interested in art, music, or creative writing',
      cluster: 'creative',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 5,
      question: 'I like organizing events and leading teams',
      cluster: 'leadership',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 6,
      question: 'I enjoy conducting experiments and scientific research',
      cluster: 'analytical',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 7,
      question: 'I prefer working with computers and technology',
      cluster: 'technical',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 8,
      question: 'I am interested in understanding human behavior and psychology',
      cluster: 'social',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 9,
      question: 'I enjoy designing and creating visual content',
      cluster: 'creative',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
    {
      id: 10,
      question: 'I like managing projects and making business decisions',
      cluster: 'leadership',
      options: [
        { value: 5, label: 'Strongly Agree' },
        { value: 4, label: 'Agree' },
        { value: 3, label: 'Neutral' },
        { value: 2, label: 'Disagree' },
        { value: 1, label: 'Strongly Disagree' },
      ],
    },
  ];

  const careerClusters = {
    analytical: {
      name: 'Analytical & Scientific',
      careers: ['Data Scientist', 'Research Scientist', 'Mathematician', 'Statistician', 'Actuary'],
      description: 'You excel at logical thinking, problem-solving, and scientific analysis.',
    },
    technical: {
      name: 'Technical & Engineering',
      careers: ['Software Engineer', 'Mechanical Engineer', 'Electrical Engineer', 'Civil Engineer', 'IT Specialist'],
      description: 'You have strong technical skills and enjoy working with tools and technology.',
    },
    social: {
      name: 'Social & Helping',
      careers: ['Teacher', 'Psychologist', 'Social Worker', 'Counselor', 'Healthcare Professional'],
      description: 'You are empathetic and enjoy helping others and making a social impact.',
    },
    creative: {
      name: 'Creative & Artistic',
      careers: ['Graphic Designer', 'Content Writer', 'Musician', 'Photographer', 'Fashion Designer'],
      description: 'You have a creative mindset and enjoy expressing yourself through art.',
    },
    leadership: {
      name: 'Leadership & Business',
      careers: ['Business Manager', 'Entrepreneur', 'Marketing Manager', 'HR Manager', 'Project Manager'],
      description: 'You have strong leadership skills and enjoy managing people and projects.',
    },
  };

  const handleAnswer = (value) => {
    const newAnswers = { ...answers, [questions[currentQuestion].id]: value };
    setAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      calculateResults(newAnswers);
    }
  };

  const calculateResults = (finalAnswers) => {
    const clusterScores = {
      analytical: 0,
      technical: 0,
      social: 0,
      creative: 0,
      leadership: 0,
    };

    questions.forEach((question) => {
      const answer = finalAnswers[question.id] || 0;
      clusterScores[question.cluster] += answer;
    });

    const maxScore = Math.max(...Object.values(clusterScores));
    const normalized = {};
    Object.keys(clusterScores).forEach((key) => {
      normalized[key] = maxScore > 0 ? Math.round((clusterScores[key] / maxScore) * 100) : 0;
    });

    const sortedClusters = Object.entries(normalized)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 3)
      .map(([cluster, score]) => ({
        cluster,
        score,
        ...careerClusters[cluster],
      }));

    setResults(sortedClusters);
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const resetTest = () => {
    setCurrentQuestion(0);
    setAnswers({});
    setResults(null);
    setTestStarted(false);
  };

  if (!testStarted) {
    return (
      <div className="space-y-6 text-center">
        <motion.div 
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", duration: 0.6 }}
          className="flex justify-center mb-6"
        >
          <div className="w-20 h-20 rounded-full bg-gradient-to-r from-purple-500/20 to-cyan-500/20 flex items-center justify-center glow-violet">
            <Brain className="w-10 h-10 text-cyan-400" />
          </div>
        </motion.div>
        <motion.h2 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-2xl font-semibold text-white"
        >
          Interest Assessment Test
        </motion.h2>
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-gray-300 max-w-2xl mx-auto"
        >
          Take this 10-question aptitude test to discover your career interests and get personalized 
          career recommendations based on your personality and preferences.
        </motion.p>
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="glass rounded-lg p-4 max-w-2xl mx-auto glow-cyan"
        >
          <p className="text-sm text-gray-300">
            <strong className="text-cyan-400">Instructions:</strong> Answer each question honestly based on your true interests 
            and preferences. There are no right or wrong answers.
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Button variant="primary" onClick={() => setTestStarted(true)}>
            Start Test
          </Button>
        </motion.div>
      </div>
    );
  }

  if (results) {
    return (
      <div className="space-y-6">
        <div className="text-center mb-8">
          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", duration: 0.6 }}
            className="flex justify-center mb-4"
          >
            <CheckCircle className="w-16 h-16 text-green-400" />
          </motion.div>
          <motion.h2 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-2xl font-semibold text-white mb-2"
          >
            Test Complete!
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-gray-300"
          >
            Here are your top career clusters based on your interests
          </motion.p>
        </div>

        {results.map((result, index) => (
          <motion.div 
            key={index} 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 + 0.3 }}
            className="glass rounded-lg p-6 glow-violet hover:glow-cyan transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-xl font-semibold text-white">{result.name}</h3>
                  <span className="px-3 py-1 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 border border-purple-500/30 rounded-full text-sm text-cyan-400">
                    Rank #{index + 1}
                  </span>
                </div>
                <p className="text-gray-300 text-sm mb-4">{result.description}</p>
              </div>
              <div className="ml-4 text-3xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                {result.score}%
              </div>
            </div>

            <div className="mb-4">
              <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${result.score}%` }}
                  transition={{ duration: 1, delay: index * 0.1 + 0.5 }}
                  className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"
                />
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-300 mb-2">Recommended Careers:</p>
              <div className="flex flex-wrap gap-2">
                {result.careers.map((career, idx) => (
                  <span key={idx} className="px-3 py-1 bg-blue-500/10 border border-blue-500/30 rounded-full text-xs text-blue-400">
                    {career}
                  </span>
                ))}
              </div>
            </div>
          </motion.div>
        ))}

        <div className="glass rounded-lg p-4 glow-cyan">
          <p className="text-sm text-gray-300">
            <strong className="text-cyan-400">Next Steps:</strong> Explore the careers listed above and research educational 
            pathways that align with your interests. Consider talking to professionals in these fields 
            to gain more insights.
          </p>
        </div>

        <div className="text-center">
          <Button variant="secondary" onClick={resetTest}>
            Retake Test
          </Button>
        </div>
      </div>
    );
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="space-y-6">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-xl font-semibold text-white">
            Question {currentQuestion + 1} of {questions.length}
          </h2>
          <span className="text-sm text-gray-400">{Math.round(progress)}% Complete</span>
        </div>
        <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
            className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"
          />
        </div>
      </div>

      <motion.div 
        key={currentQuestion}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        className="glass rounded-lg p-8 glow-violet"
      >
        <p className="text-lg text-white mb-6">{questions[currentQuestion].question}</p>

        <div className="space-y-3">
          {questions[currentQuestion].options.map((option, index) => (
            <motion.button
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => handleAnswer(option.value)}
              className={`w-full p-4 text-left rounded-lg border transition-all duration-300 ${
                answers[questions[currentQuestion].id] === option.value
                  ? 'bg-gradient-to-r from-purple-500/20 to-cyan-500/20 border-cyan-500 text-white'
                  : 'bg-white/5 border-white/10 text-gray-300 hover:bg-white/10 hover:border-cyan-500/50'
              }`}
            >
              {option.label}
            </motion.button>
          ))}
        </div>
      </motion.div>

      <div className="flex justify-between">
        <Button
          variant="secondary"
          onClick={handlePrevious}
          disabled={currentQuestion === 0}
        >
          Previous
        </Button>
        <Button variant="secondary" onClick={resetTest}>
          Cancel Test
        </Button>
      </div>
    </div>
  );
};

export default InterestTest;
