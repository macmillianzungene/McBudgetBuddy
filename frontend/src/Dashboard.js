import React, { useState, useEffect } from "react";
import { addExpense, setGoal } from "./api"; // Import API functions
import axios from "axios";

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [goals, setGoals] = useState([]);
  const [newExpense, setNewExpense] = useState({
    amount: "",
    category: "",
    date: "",
  });
  const [newGoal, setNewGoal] = useState({ goal_amount: "", category: "" });

  // Simulating getting the user_id, adjust as needed for your app (could come from local storage, context, etc.)
  const getUserId = () => {
    // Replace this with your real user id logic
    return 1; // Assuming a logged-in user with id 1
  };

  // Fetch expenses and goals from backend when component mounts
  useEffect(() => {
    const userId = getUserId(); // Make sure you're fetching for the correct user
    axios
      .get(`http://127.0.0.1:5000/get_expenses?user_id=${userId}`)
      .then((response) => setExpenses(response.data))
      .catch((error) => console.error("Error fetching expenses:", error));

    axios
      .get(`http://127.0.0.1:5000/get_goals?user_id=${userId}`)
      .then((response) => setGoals(response.data))
      .catch((error) => console.error("Error fetching goals:", error));
  }, []);

  // Add an expense
  const handleAddExpense = async (e) => {
    e.preventDefault();
    try {
      const user_id = getUserId(); // Get the user id
      const expenseData = { ...newExpense, user_id }; // Add user_id to the expense data
      const response = await addExpense(expenseData);
      setExpenses([...expenses, response.data]); // Update the expenses state with the new expense
      setNewExpense({ amount: "", category: "", date: "" }); // Reset the input fields
    } catch (error) {
      console.error("Error adding the expense", error);
    }
  };

  // Set a new financial goal
  const handleSetGoal = async (e) => {
    e.preventDefault();
    try {
      const user_id = getUserId(); // Get the user id
      const goalData = { ...newGoal, user_id }; // Add user_id to the goal data
      const response = await setGoal(goalData);
      setGoals([...goals, response.data]); // Update the goals state with the new goal
      setNewGoal({ goal_amount: "", category: "" }); // Reset the input fields
    } catch (error) {
      console.error("Error setting the goal", error);
    }
  };

  return (
    <div>
      <h2>Your Dashboard</h2>

      <h3>Log a New Expense</h3>
      <form onSubmit={handleAddExpense}>
        <input
          type="number"
          placeholder="Amount"
          value={newExpense.amount}
          onChange={(e) =>
            setNewExpense({ ...newExpense, amount: e.target.value })
          }
          required
        />
        <input
          type="text"
          placeholder="Category"
          value={newExpense.category}
          onChange={(e) =>
            setNewExpense({ ...newExpense, category: e.target.value })
          }
          required
        />
        <input
          type="date"
          value={newExpense.date}
          onChange={(e) =>
            setNewExpense({ ...newExpense, date: e.target.value })
          }
          required
        />
        <button type="submit">Add Expense</button>
      </form>

      <h3>Set a New Goal</h3>
      <form onSubmit={handleSetGoal}>
        <input
          type="number"
          placeholder="Target Amount"
          value={newGoal.goal_amount}
          onChange={(e) =>
            setNewGoal({ ...newGoal, goal_amount: e.target.value })
          }
          required
        />
        <input
          type="text"
          placeholder="Category"
          value={newGoal.category}
          onChange={(e) => setNewGoal({ ...newGoal, category: e.target.value })}
          required
        />
        <button type="submit">Set Goal</button>
      </form>

      <h3>Your Expenses</h3>
      <ul>
        {expenses.map((expense, index) => (
          <li key={index}>
            {expense.category}: ${expense.amount} on {expense.date}
          </li>
        ))}
      </ul>

      <h3>Your Goals</h3>
      <ul>
        {goals.map((goal, index) => (
          <li key={index}>
            {goal.category}: ${goal.goal_amount}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;

