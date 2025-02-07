from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (useful for frontend/backend communication)

@app.route('/')
def home():
    return "Budget Buddy Backend"

# Database connection helper function
def get_db():
    conn = sqlite3.connect('budget_buddy.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        username = data['username']
        password = data['password']
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        username = data['username']
        password = data['password']
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password_hash'], password):        
        return jsonify({"message": "Login successful"}), 200   
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Add Expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()

    try:
        amount = data['amount']
        category = data['category']
        date = data['date']
        user_id = data['user_id']
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, date, user_id) VALUES (?, ?, ?, ?)",
                   (amount, category, date, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"}), 201

# Get Expenses
@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing field: user_id"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, category, date FROM expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()
    conn.close()

    expenses_list = [{"id": row["id"], "amount": row["amount"], "category": row["category"], "date": row["date"]} for row in expenses]

    return jsonify(expenses_list), 200

# Set Goal
@app.route('/set_goal', methods=['POST'])
def set_goal():
    data = request.json
    try:
        goal_amount = data['goal_amount']
        category = data['category']
        user_id = data['user_id']
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO goals (goal_amount, category, user_id) VALUES (?, ?, ?)",
                   (goal_amount, category, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Goal set successfully"}), 201

# Get Goals
@app.route('/get_goals', methods=['GET'])
def get_goals():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing field: user_id"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, goal_amount, category FROM goals WHERE user_id = ?", (user_id,))
    goals = cursor.fetchall()
    conn.close()

    goals_list = [{"id": row["id"], "goal_amount": row["goal_amount"], "category": row["category"]} for row in goals]

    return jsonify(goals_list), 200

if __name__ == '__main__':
    app.run(debug=True)

