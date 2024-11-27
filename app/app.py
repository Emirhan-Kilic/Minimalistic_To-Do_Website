import re
import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'

mysql = MySQL(app)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('tasks'))
        else:
            message = 'Please enter correct username / password !'
    return render_template('login.html', message = message)


@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'

        elif not username or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (id, username, email, password) VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':

        message = 'Please fill all the fields!'
    return render_template('register.html', message = message)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    message = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    user_id = session['userid']
    username = session['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('''
        SELECT Task.id, Task.description, Task.status, Task.task_type, Task.creation_time, 
        Task.title, Task.completion_time, Task.deadline
        FROM Task
        WHERE Task.user_id = %s AND Task.status = "Done"
        ORDER BY Task.completion_time DESC
    ''', (user_id,))

    doneTasks = cursor.fetchall()

    cursor.execute('''
        SELECT Task.id, Task.description, Task.status, Task.task_type, Task.creation_time, 
        Task.title, Task.completion_time, Task.deadline
        FROM Task
        WHERE Task.user_id = %s AND Task.status != "Done"
        ORDER BY Task.deadline ASC
    ''', (user_id,))

    todoTasks = cursor.fetchall()

    cursor.execute('SELECT * FROM TaskType')
    task_types = cursor.fetchall()

    if request.method == 'POST':
        if 'complete_task' in request.form:
            task_id = request.form['task_id']
            cursor.execute('''
                UPDATE Task
                SET status = "Done", completion_time = NOW()
                WHERE id = %s
            ''', (task_id,))
            mysql.connection.commit()
            message = 'Task Completed!'
            return redirect(url_for('tasks'))

        if 'edit_task' in request.form:
            task_id = request.form['task_id']
            title = request.form['title']
            description = request.form['description']
            task_type = request.form['task_type']
            deadline = request.form['deadline']
            cursor.execute('''
                UPDATE Task
                SET deadline = %s, title = %s,  task_type = %s, description = %s,
                WHERE id = %s
            ''', (deadline, title,  task_type, description, task_id))
            mysql.connection.commit()
            return redirect(url_for('tasks'))

        if 'delete_task' in request.form:
            task_id = request.form['task_id']
            cursor.execute('DELETE FROM Task WHERE id = %s', (task_id,))
            mysql.connection.commit()
            message = 'Task Deleted!'
            return redirect(url_for('tasks'))

        if 'create_task' in request.form:
            title = request.form['title']
            description = request.form['description']
            task_type = request.form['task_type']
            deadline = request.form['deadline']
            cursor.execute('''
                INSERT INTO Task ( creation_time, status, deadline, title, task_type,description , user_id )
                VALUES (NOW(), 'Todo', %s, %s, %s, %s,  %s)
            ''', (deadline, title, task_type, description, user_id))
            mysql.connection.commit()
            message = 'Task created'
            return redirect(url_for('tasks'))

    return render_template('tasks.html', doneTasks=doneTasks, todoTasks=todoTasks, task_types=task_types, message=message, username=username)




@app.route('/analysis', methods =['GET', 'POST'])
def analysis():
    message = ''
    if not 'loggedin' in session:
        return redirect(url_for('login'))

    user_id = session['userid']
    username = session['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('''
        SELECT Task.status, Task.task_type, 
        Task.title, Task.deadline
        FROM Task
        WHERE Task.user_id = %s 
        ORDER BY Task.deadline ASC
    ''', (user_id,))
    allTasks1 = cursor.fetchall()

    cursor.execute('''
        SELECT Task.title, Task.completion_time, 
               DATEDIFF(Task.completion_time, Task.creation_time) AS time_spent
        FROM Task
        WHERE Task.user_id = %s AND Task.status = "Done"
        ORDER BY Task.completion_time ASC
    ''', (user_id,))
    completedTasks2 = cursor.fetchall()

    cursor.execute('''
        SELECT Task.title, Task.task_type, Task.deadline
        FROM Task
        WHERE Task.user_id = %s and Task.status = "Todo"
        ORDER BY Task.deadline ASC
    ''', (user_id,))
    uncompletedTasks3 = cursor.fetchall()

    cursor.execute('''
        SELECT Task.title, 
               DATEDIFF(Task.completion_time, Task.deadline) AS latency
        FROM Task
        WHERE Task.user_id = %s AND Task.status = "Done" AND Task.deadline < Task.completion_time
        ORDER BY Task.completion_time ASC
    ''', (user_id,))
    latencyTasks4 = cursor.fetchall()

    cursor.execute('''
        SELECT Task.task_type, COUNT(*) AS cnt
        FROM Task
        WHERE Task.user_id = %s AND Task.status = "Done"
        GROUP BY Task.task_type
        ORDER BY cnt DESC
    ''', (user_id,))
    numberOfCompletedTask5 = cursor.fetchall()

    return render_template('analysis.html', allTasks1 = allTasks1, completedTasks2 = completedTasks2, uncompletedTasks3=uncompletedTasks3, latencyTasks4=latencyTasks4, numberOfCompletedTask5=numberOfCompletedTask5, message=message, username=username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
