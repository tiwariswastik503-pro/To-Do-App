from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
import mysql.connector # type: ignore

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for flash messages

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tiwari160355",  # replace with your password
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
