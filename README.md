Step-by-Step Guide to Build the Flask To-Do List App


🪜 Step 1: Install Prerequisites



Make sure you have the following installed:

Python 3.x

MySQL Server

pip (Python package manager)

You can check using:

python --version
mysql --version


If you don’t have them, install from:

Python

MySQL


🧰 Step 2: Create Project Folder


Create a new folder for your project:

mkdir flask_todo_app
cd flask_todo_app


Inside, create these folders:

flask_todo_app/
├── app.py
├── templates/
│   ├── index.html
│   └── edit.html
├── static/
│   └── style.css



🐍 Step 3: Set Up a Virtual Environment



It’s best to isolate your project dependencies.

python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate


📦 Step 4: Install Required Packages


Install Flask and MySQL Connector:

pip install flask mysql-connector-python


(Optional) Freeze dependencies:

pip freeze > requirements.txt


🗃️ Step 5: Set Up the MySQL Database


Open MySQL terminal or a client like phpMyAdmin and run:

CREATE DATABASE todo_db;
USE todo_db;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status ENUM('pending', 'completed') DEFAULT 'pending'
);

⚙️ Step 6: Create the Flask Application

Create a file named app.py and paste this code:

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourMySQLPassword",  # Replace with your password
    database="todo_db"
)
cursor = db.cursor(dictionary=True)

# Home page - show all tasks
@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

# Add new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    if title:
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        db.commit()
        flash("Task added successfully!", "success")
    else:
        flash("Task cannot be empty!", "error")
    return redirect(url_for('index'))

# Mark as completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    cursor.execute("UPDATE tasks SET status='completed' WHERE id=%s", (task_id,))
    db.commit()
    flash("Task marked as completed!", "info")
    return redirect(url_for('index'))

# Edit task page
@app.route('/edit/<int:task_id>')
def edit_task(task_id):
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    task = cursor.fetchone()
    return render_template('edit.html', task=task)

# Update task
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    title = request.form['title']
    cursor.execute("UPDATE tasks SET title=%s WHERE id=%s", (title, task_id))
    db.commit()
    flash("Task updated!", "success")
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    db.commit()
    flash("Task deleted!", "warning")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


🧾 Step 7: Create HTML Templates


🏠 templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h2 class="mb-4 text-center">📝 My To-Do List</h2>

        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        {% endwith %}

        <form action="/add" method="POST" class="mb-3 d-flex">
            <input type="text" name="title" class="form-control me-2" placeholder="Add a new task">
            <button class="btn btn-primary">Add</button>
        </form>

        <ul class="list-group">
            {% for task in tasks %}
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span class="{% if task.status == 'completed' %}text-decoration-line-through text-success{% endif %}">
                    {{ task.title }}
                </span>
                <div>
                    <a href="/complete/{{ task.id }}" class="btn btn-sm btn-success">✔</a>
                    <a href="/edit/{{ task.id }}" class="btn btn-sm btn-warning">✏️</a>
                    <a href="/delete/{{ task.id }}" class="btn btn-sm btn-danger">🗑</a>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>

✏️ templates/edit.html
<!DOCTYPE html>
<html>
<head>
    <title>Edit Task</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h3>Edit Task</h3>
        <form action="/update/{{ task.id }}" method="POST">
            <input type="text" name="title" value="{{ task.title }}" class="form-control mb-3" required>
            <button class="btn btn-primary">Update</button>
            <a href="/" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</body>
</html>


▶️ Step 8: Run the Flask App


Run your app with:

python app.py


You’ll see something like:

* Running on http://127.0.0.1:5000/


Now open your browser and go to 👉 http://127.0.0.1:5000


✅ Step 9: Test All Features


Try:

Adding a new task

Marking it complete

Editing the title

Deleting a task

Flash messages should confirm each action.
