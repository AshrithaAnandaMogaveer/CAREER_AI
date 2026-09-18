/**
 * Generic Scoring Engine
 * Reusable weighted scoring system for career guidance recommendations
 * 
 * This engine can be used across different guidance modules (After 10th, After 12th, etc.)
 * by providing different weight matrices and rules.
 */

/**
 * Calculate weighted scores for multiple options based on user input
 * 
 * @param {Object} config - Configuration object
 * @param {Object} config.userInput - User's selections and preferences
 * @param {Array<string>} config.userInput.selectedItems - Items selected by user (e.g., interests)
 * @param {string} config.userInput.multiplierKey - Key for multiplier (e.g., strengthLevel)
 * @param {string} config.userInput.bonusKey - Key for bonus calculation (e.g., learningStyle)
 * @param {Object} config.weightMatrix - Weight matrix mapping options to items
 * @param {Object} config.multipliers - Multiplier values for different levels
 * @param {Object} config.bonusRules - Bonus rules for each option
 * @returns {Object} Calculated scores for each option
 */
export function calculateWeightedScores({
  userInput,
  weightMatrix,
  multipliers,
  bonusRules,
}) {
  const { selectedItems, multiplierKey, bonusKey } = userInput;
  
  // Get multiplier value
  const multiplierValue = multipliers[userInput[multiplierKey]] || 1;
  
  // Calculate base scores for each option
  const scores = {};
  
  Object.keys(weightMatrix).forEach((option) => {
    let score = 0;
    
    // Calculate weighted score based on selected items
    selectedItems.forEach((item) => {
      const weight = weightMatrix[option][item] || 0;
      score += weight * multiplierValue;
    });
    
    // Apply bonus if applicable
    if (bonusRules && bonusRules[option] && userInput[bonusKey]) {
      const bonus = bonusRules[option][userInput[bonusKey]] || 0;
      score += bonus;
    }
    
    scores[option] = score;
  });
  
  return scores;
}

/**
 * Normalize scores to percentages
 * 
 * @param {Object} scores - Raw scores for each option
 * @returns {Object} Normalized scores as percentages
 */
export function normalizeScores(scores) {
  const maxScore = Math.max(...Object.values(scores));
  const normalizedScores = {};
  
  Object.keys(scores).forEach((option) => {
    normalizedScores[option] = maxScore > 0 
      ? Math.round((scores[option] / maxScore) * 100) 
      : 0;
  });
  
  return normalizedScores;
}

/**
 * Rank options by score
 * 
 * @param {Object} scores - Scores for each option
 * @param {number} topN - Number of top results to return (default: all)
 * @returns {Array<Object>} Ranked options with scores
 */
export function rankByScore(scores, topN = null) {
  const ranked = Object.entries(scores)
    .map(([option, score]) => ({ option, score }))
    .sort((a, b) => b.score - a.score);
  
  return topN ? ranked.slice(0, topN) : ranked;
}

/**
 * Complete scoring pipeline
 * Calculates, normalizes, and ranks scores in one call
 * 
 * @param {Object} config - Configuration object (same as calculateWeightedScores)
 * @param {number} topN - Number of top results to return
 * @returns {Array<Object>} Top N ranked options with normalized scores
 */
export function calculateScores(config, topN = null) {
  // Step 1: Calculate raw weighted scores
  const rawScores = calculateWeightedScores(config);
  
  // Step 2: Normalize to percentages
  const normalizedScores = normalizeScores(rawScores);
  
  // Step 3: Rank by score
  const ranked = rankByScore(rawScores, topN);
  
  // Step 4: Attach normalized scores to ranked results
  const results = ranked.map((item) => ({
    option: item.option,
    rawScore: item.score,
    normalizedScore: normalizedScores[item.option],
  }));
  
  return results;
}

/**
 * Validate scoring configuration
 * 
 * @param {Object} config - Configuration object
 * @returns {Object} Validation result
 */
export function validateScoringConfig(config) {
  const errors = [];
  
  if (!config.userInput) {
    errors.push('userInput is required');
  }
  
  if (!config.weightMatrix || Object.keys(config.weightMatrix).length === 0) {
    errors.push('weightMatrix is required and must not be empty');
  }
  
  if (!config.multipliers) {
    errors.push('multipliers object is required');
  }
  
  if (config.userInput && (!config.userInput.selectedItems || config.userInput.selectedItems.length === 0)) {
    errors.push('At least one item must be selected');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
}

/**
 * Calculate contribution of each selected item to an option
 * Useful for generating explanations
 * 
 * @param {string} option - The option to analyze
 * @param {Array<string>} selectedItems - Items selected by user
 * @param {Object} weightMatrix - Weight matrix
 * @returns {Array<Object>} Items sorted by contribution
 */
export function getItemContributions(option, selectedItems, weightMatrix) {
  const optionWeights = weightMatrix[option] || {};
  
  const contributions = selectedItems
    .map((item) => ({
      item,
      weight: optionWeights[item] || 0,
    }))
    .filter((contrib) => contrib.weight > 0)
    .sort((a, b) => b.weight - a.weight);
  
  return contributions;
}

/**
 * Utility: Find options that align with a specific criterion
 * 
 * @param {Object} weightMatrix - Weight matrix
 * @param {string} item - Item to check alignment for
 * @param {number} minWeight - Minimum weight threshold
 * @returns {Array<string>} Options that align with the item
 */
export function findAlignedOptions(weightMatrix, item, minWeight = 1) {
  const aligned = [];
  
  Object.keys(weightMatrix).forEach((option) => {
    if (weightMatrix[option][item] >= minWeight) {
      aligned.push(option);
    }
  });
  
  return aligned;
}

export default {
  calculateWeightedScores,
  normalizeScores,
  rankByScore,
  calculateScores,
  validateScoringConfig,
  getItemContributions,
  findAlignedOptions,
};
