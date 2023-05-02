import asyncio
import logging
import threading
from flask import Flask, jsonify, abort, make_response, request, url_for
from time import sleep

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

warning_colour = '\033[93m'
end_colour = '\033[0m'
blue = '\033[94m'
cyan = '\033[96m'
green = '\033[92m'
def task_with_uri(task):
    new_task = {}
    for key in task:
        if key == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[key] = task[key]
    return new_task

def hello():
    logging.info(f"{blue}Starting fast operation...{end_colour}")
    # await asyncio.sleep(3)
    sleep(1)
    logging.info(f"{blue}Short completed{end_colour}")
    return 1

def hello_stupid():
    logging.info(f"{green}Starting long operation...{end_colour}")
    sleep(5) 
    logging.info(f"{green}Long completed{end_colour}")
    return 1 

# async demo
@app.route('/api/async/<int:func_id>', methods=['GET'])
def async_call(func_id):
    thread = threading.current_thread().name
    logging.info(f"{warning_colour}In thread: {thread}{end_colour}") 
    # print(f'Bla bla bla: {threading.current_thread().name}') 
    # result = await hello()
    result = hello_stupid() if func_id == 1 else hello()
    return jsonify({"result": result})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # sleep(5)
    # return jsonify({'tasks': tasks}) 
    return jsonify({'tasks': [task_with_uri(task) for task in tasks]})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]    
    if len(task) == 0:
        abort(404)
    return jsonify(task[0])

@app.route('/api/tasks', methods=['POST'])
def post_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {'id': tasks[-1]['id'] + 1, 
            'title': request.json['title'],
            'description': request.json.get('description', ''),
            'done': False } 
    tasks.append(task)
    return jsonify({'task' : task}), 201

@app.errorhandler(404)
def task_not_found(error):
    return make_response(jsonify({'error' : 'Task not found'}), 404)

def main():
    level = logging.DEBUG
    fmt = '[%(levelname)s] - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    app.run()

if __name__ == '__main__':
    main()
