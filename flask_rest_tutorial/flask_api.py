from flask import Flask, jsonify, abort
from flask_restful import Resource, Api, reqparse
import logging
import asyncio

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

# def task_with_uri(task):
#     new_task = {}
#     for key in task:
#         if key == 'id':
#             new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
#         else:
#             new_task[key] = task[key]
#     return new_task

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json', help='Must be bool')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) != 1:
            raise Exception('Oh no!')
        return jsonify(f'task: {task[0]}')
    
    def put(self, id):
        found_tasks = [task for task in tasks if task['id'] == id]
        if len(found_tasks) != 1:
            abort(404)
        task = found_tasks[0] 
        args = self.reqparse.parse_args()
        for key, value in args.items():
            logging.info(f"[DEBUG] params are {key} : {value}")
            if value != None:
                task[key] = value
        return {'task' : task}, 201
        

    def delete(self, id):
        pass
        
class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default='', location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return jsonify(f"tasks: {tasks}")

class UserAPI(Resource):
    def get(self, id):
        pass
    
    def put(self, id):
        pass

    def delete(self, id):
        pass

def main():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(UserAPI, '/api/users/<int:id>', endpoint='user')
    api.add_resource(TaskAPI, '/api/tasks/<int:id>', endpoint='task')
    api.add_resource(TaskListAPI, '/api/tasks', endpoint='tasks')
    app.run()

if __name__ == '__main__':
    main()
