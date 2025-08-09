# Comments made for me - self learning purposes for flask application

# libraries used:
# render_template - display HTML templates
# request - access data sent by the user
# redirect - direct the user to a different page
# url_for - generate URLs for the application
# jsonify - convert data to JSON format
# json - for working with JSON data
# os - for interacting with the operating system
# datetime - for working with dates and times
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

# Create a Flask application instance - telling flask to use this file as the main application
app = Flask(__name__)
# name of the file where tasks will be stored
TASKS_FILE = 'tasks.json'

def load_tasks(): # Load tasks from the JSON file.
    if os.path.exists(TASKS_FILE): # check if the file/folders exists in the computer
        with open(TASKS_FILE, 'r', encoding='utf-8') as f: # safe safe way to open a file, 'r' means read mode
            return json.load(f) # return the content of the file as a Python object
    return []

def save_tasks(tasks): # save tasks to the JSON file.
    with open(TASKS_FILE, 'w', encoding='utf-8') as f: # w means write mode, it will overwrite the file if it exists
        json.dump(tasks, f, ensure_ascii=False, indent=2) # ensure_ascii=False allows non-ASCII characters to be written correctly

@app.route('/') # home page - displays all tasks, @ - a way to change the behavior of a function
def index():
    tasks = load_tasks() # calls the function we created before (to load tasks)
    return render_template('index.html', tasks=tasks) # take html file and display it, passing the tasks to the template

@app.route('/add', methods=['POST']) # add a new task, only accepts POST requests
def add_task():
    task_text = request.form.get('task')
    if task_text:
        tasks = load_tasks()
        new_task = {
            'id': len(tasks) + 1,
            'text': task_text,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect(url_for('index'))