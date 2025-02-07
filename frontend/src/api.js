import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';  // Flask backend URL

// Register user
export const registerUser = (userData) => {
  return axios.post(`${API_URL}/register`, userData);
};

// Login user
export const loginUser = (userData) => {
  return axios.post(`${API_URL}/login`, userData);
};

// Add expense
export const addExpense = (expenseData) => {
  return axios.post(`${API_URL}/add_expense`, expenseData);
};

// Set goal
export const setGoal = (goalData) => {
  return axios.post(`${API_URL}/set_goal`, goalData);
};

// Fetch expenses
export const getExpenses = () => {
  return axios.get(`${API_URL}/get_expenses`);
};

// Fetch goals
export const getGoals = () => {
  return axios.get(`${API_URL}/get_goals`);
};

