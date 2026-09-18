/**
 * After 10th Guidance Scoring Algorithm
 * Calculates stream recommendations based on interests, strengths, and learning style
 * Uses the generic scoringEngine for calculation logic
 */

import { calculateScores, getItemContributions } from './scoringEngine';

// Stream weight matrix - defines how each interest area contributes to each stream
const STREAM_WEIGHTS = {
  Science: {
    'Logical/Math': 3,
    'Science': 3,
    'Technology': 2,
    'Business': 0,
    'Creativity': 0,
    'Communication': 1,
  },
  Commerce: {
    'Logical/Math': 2,
    'Science': 0,
    'Technology': 1,
    'Business': 3,
    'Creativity': 1,
    'Communication': 2,
  },
  Arts: {
    'Logical/Math': 0,
    'Science': 0,
    'Technology': 1,
    'Business': 1,
    'Creativity': 3,
    'Communication': 3,
  },
};

// Strength level multipliers
const STRENGTH_MULTIPLIERS = {
  Low: 1,
  Medium: 2,
  High: 3,
};

// Learning style bonuses for each stream
const LEARNING_STYLE_BONUS = {
  Science: {
    Practical: 2,
    Theoretical: 3,
    Creative: 1,
  },
  Commerce: {
    Practical: 3,
    Theoretical: 2,
    Creative: 1,
  },
  Arts: {
    Practical: 1,
    Theoretical: 1,
    Creative: 3,
  },
};

// Stream descriptions
const STREAM_INFO = {
  Science: {
    name: 'Science Stream (PCM/PCB)',
    description: 'Perfect for students interested in engineering, medicine, and research',
    careers: ['Engineering', 'Medicine', 'Research', 'Technology', 'Architecture'],
  },
  Commerce: {
    name: 'Commerce Stream',
    description: 'Ideal for careers in business, finance, and accounting',
    careers: ['Business', 'Finance', 'Accounting', 'Economics', 'Management'],
  },
  Arts: {
    name: 'Arts/Humanities Stream',
    description: 'Best for creative minds interested in social sciences and languages',
    careers: ['Design', 'Media', 'Psychology', 'Law', 'Education', 'Social Work'],
  },
};

/**
 * Calculate stream scores based on user inputs
 * @param {Object} userInput - User's selections
 * @param {Array<string>} userInput.interests - Selected interest areas
 * @param {string} userInput.strengthLevel - Strength level (Low/Medium/High)
 * @param {string} userInput.learningStyle - Learning style preference
 * @returns {Array<Object>} Ranked stream recommendations
 */
export function calculateAfter10thResults(userInput) {
  const { interests, strengthLevel, learningStyle } = userInput;

  // Validate inputs
  if (!interests || interests.length === 0) {
    throw new Error('Please select at least one interest area');
  }
  if (!strengthLevel) {
    throw new Error('Please select your strength level');
  }
  if (!learningStyle) {
    throw new Error('Please select your learning style');
  }

  // Use generic scoring engine
  const scoringConfig = {
    userInput: {
      selectedItems: interests,
      multiplierKey: 'strengthLevel',
      bonusKey: 'learningStyle',
      strengthLevel,
      learningStyle,
    },
    weightMatrix: STREAM_WEIGHTS,
    multipliers: STRENGTH_MULTIPLIERS,
    bonusRules: LEARNING_STYLE_BONUS,
  };

  // Calculate scores using the generic engine (returns top 3 by default)
  const rankedScores = calculateScores(scoringConfig, 3);

  // Transform results to match expected output format
  const results = rankedScores.map((item) => {
    const stream = item.option;
    
    // Generate dynamic explanation
    const explanation = generateExplanation(
      stream,
      interests,
      strengthLevel,
      learningStyle,
      item.rawScore
    );

    return {
      id: stream.toLowerCase(),
      name: STREAM_INFO[stream].name,
      description: STREAM_INFO[stream].description,
      careers: STREAM_INFO[stream].careers,
      score: item.normalizedScore,
      rawScore: item.rawScore,
      reasoning: explanation,
    };
  });

  return results;
}

/**
 * Generate dynamic explanation for stream recommendation
 * @param {string} stream - Stream name
 * @param {Array<string>} interests - Selected interests
 * @param {string} strengthLevel - Strength level
 * @param {string} learningStyle - Learning style
 * @param {number} score - Calculated score
 * @returns {string} Explanation text
 */
function generateExplanation(stream, interests, strengthLevel, learningStyle, score) {
  // Use scoring engine utility to get interest contributions
  const contributions = getItemContributions(stream, interests, STREAM_WEIGHTS);

  if (contributions.length === 0) {
    return `This stream has limited alignment with your selected interests.`;
  }

  // Extract relevant interests (those that contributed)
  const relevantInterests = contributions.map((c) => c.item);

  // Build explanation
  let explanation = `Based on your ${strengthLevel.toLowerCase()} strength in `;
  
  if (relevantInterests.length === 1) {
    explanation += `${relevantInterests[0]}`;
  } else if (relevantInterests.length === 2) {
    explanation += `${relevantInterests[0]} and ${relevantInterests[1]}`;
  } else {
    explanation += `${relevantInterests.slice(0, -1).join(', ')}, and ${relevantInterests[relevantInterests.length - 1]}`;
  }

  // Add learning style bonus mention
  const learningBonus = LEARNING_STYLE_BONUS[stream][learningStyle];
  if (learningBonus >= 2) {
    explanation += `, and your ${learningStyle.toLowerCase()} learning style aligns well with this stream`;
  }

  explanation += `.`;

  return explanation;
}

/**
 * Validate user input before processing
 * @param {Object} userInput - User's selections
 * @returns {Object} Validation result
 */
export function validateAfter10thInput(userInput) {
  const errors = [];

  if (!userInput.interests || userInput.interests.length === 0) {
    errors.push('Please select at least one interest area');
  }

  if (!userInput.strengthLevel) {
    errors.push('Please select your strength level');
  }

  if (!userInput.learningStyle) {
    errors.push('Please select your learning style');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
