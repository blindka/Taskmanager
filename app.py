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

@app.route('/add', methods=['POST']) 
def add_task(): # add a new task, only accepts POST requests
    task_text = request.form.get('task') # looking 'task' field in the form data submitted by the user
    if task_text:
        tasks = load_tasks()
        new_task = {
            'id': len(tasks) + 1,
            'text': task_text, # the text that the user entered in the form
            'completed': False, # new task is not completed by default
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S') # current date and time when the task was created
        }
        tasks.append(new_task) # add the new task to the list of tasks
        save_tasks(tasks)
    return redirect(url_for('index')) # redirect the user back to the home page after adding the task

@app.route('/complete/<int:task_id>') # complete a task by its ID
def complete_task(task_id): # mark a task as completed
    tasks = load_tasks()
    for task in tasks: # over each task in the list
        if task['id'] == task_id: # check if it is the task we want to complete
            task['completed'] = True # mark the task as completed
            break
    save_tasks(tasks) # save the updated tasks list
    return redirect(url_for('index')) # redirect the user back to the home page after completing the task to see the changes

@app.route('/delete/<int:task_id>') # delete a task by its ID
def delete_task(task_id): # delete a task by its ID
    tasks = load_tasks() 
    tasks = [task for task in tasks if task['id'] != task_id] # create a new list of tasks that does not include the task with the given ID
    save_tasks(tasks) # save the updated tasks list without the deleted task
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST']) # edit a task by its ID
def edit_task(task_id):
    new_text = request.form.get('new_text')
    if new_text:  # checking the text isn't empty
        tasks = load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['text'] = new_text
                break
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/favicon.ico') # every browser automatically requests a favicon, this route handles that request
def favicon(): # handle the request for the favicon
    return send_from_directory( # send the favicon file from the static directory
        directory=app.static_folder, 
        path='images/taskmanager_icon.png',
        mimetype='image/png'
    )
if __name__ == '__main__': # run the application
    # tell if there is an error in the code, display details information in the browser and refresh the page automatically when changes are made
    app.run(debug=True)