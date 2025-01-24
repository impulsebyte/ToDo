import json
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# File to store todos
TODO_FILE = 'todos.json'

# Helper function to load todos from file
def load_todos():
    try:
        with open(TODO_FILE, 'r') as file:
            data = file.read().strip()
            return json.loads(data) if data else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Helper function to save todos to file
def save_todos(todos):
    with open(TODO_FILE, 'w') as file:
        json.dump(todos, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Date parameter is required"}), 400

    todos = load_todos()
    return jsonify(todos.get(date, []))

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.json
    date = data.get('date')
    todo = data.get('todo')

    if not date or not todo:
        return jsonify({"error": "Date and todo are required"}), 400

    todos = load_todos()
    if date not in todos:
        todos[date] = []

    todos[date].append(todo)
    save_todos(todos)
    return jsonify({"message": "Todo added successfully"}), 201

@app.route('/api/todos', methods=['DELETE'])
def delete_todo():
    data = request.json
    date = data.get('date')
    todo = data.get('todo')

    if not date or not todo:
        return jsonify({"error": "Date and todo are required"}), 400

    todos = load_todos()
    if date in todos and todo in todos[date]:
        todos[date].remove(todo)
        if not todos[date]:
            del todos[date]  # Remove the date key if no todos left
        save_todos(todos)
        return jsonify({"message": "Todo deleted successfully"})

    return jsonify({"error": "Todo not found"}), 404

if __name__ == '__main__':
    # app.run(debug=True)
    gunicorn app:app
