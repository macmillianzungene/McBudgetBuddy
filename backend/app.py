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
    return conn

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']

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
    username = data['username']
    password = data['password']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Add Expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    amount = data['amount']
    category = data['category']
    date = data['date']
    user_id = data['user_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, date, user_id) VALUES (?, ?, ?, ?)", 
                   (amount, category, date, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"}), 201

# Set Goal
@app.route('/set_goal', methods=['POST'])
def set_goal():
    data = request.json
    goal_amount = data['goal_amount']
    category = data['category']
    user_id = data['user_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO goals (goal_amount, category, user_id) VALUES (?, ?, ?)", 
                   (goal_amount, category, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Goal set successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)

