import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

/**
 * Log a meal using voice input
 * @param {string} mealDescription - Description of the meal
 * @param {string} timestamp - When the meal was eaten
 * @param {number} confidence - Confidence score from speech recognition (0-1)
 * @returns {Promise<Object>} Meal log response
 */
export const logMealWithVoice = async (mealDescription, timestamp = null, confidence = 1.0) => {
  try {
    const response = await axios.post(`${API_BASE}/voice/log-meal`, {
      mealDescription: mealDescription.trim(),
      timestamp: timestamp || new Date().toISOString(),
      confidence: parseFloat(confidence)
    });
    return response.data;
  } catch (error) {
    const errorMsg = error.response?.data?.message || error.response?.data?.detail || 'Failed to log meal';
    throw new Error(errorMsg);
  }
};

/**
 * Get food suggestions for autocomplete
 * @param {string} query - Partial food name to search for
 * @returns {Promise<Array>} List of matching food suggestions
 */
export const getFoodSuggestions = async (query = '') => {
  try {
    const response = await axios.get(`${API_BASE}/voice/food-suggestions`, {
      params: { query }
    });
    return response.data.suggestions || [];
  } catch (error) {
    console.error('Failed to get food suggestions:', error);
    return [];
  }
};

/**
 * Get detailed nutrition info for a specific food
 * @param {string} foodName - Name of the food
 * @returns {Promise<Object>} Food nutritional information
 */
export const getFoodInfo = async (foodName) => {
  try {
    const response = await axios.get(`${API_BASE}/voice/food-info`, {
      params: { food_name: foodName }
    });
    return response.data;
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Food not found';
    throw new Error(errorMsg);
  }
};

/**
 * Batch log multiple meals from voice
 * @param {Array} meals - Array of meal descriptions
 * @returns {Promise<Array>} List of created meal logs
 */
export const logMultipleMeals = async (meals) => {
  try {
    const promises = meals.map(meal =>
      logMealWithVoice(
        meal.description,
        meal.timestamp,
        meal.confidence
      )
    );
    return await Promise.all(promises);
  } catch (error) {
    throw new Error('Failed to log multiple meals');
  }
};

export default {
  logMealWithVoice,
  getFoodSuggestions,
  getFoodInfo,
  logMultipleMeals
};
