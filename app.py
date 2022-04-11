from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

# list (of dictionaries) as in memory db
todos = [
    # {"name": "this is my first task"}
]


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


class TodoItem(Resource):

    @staticmethod
    def post(name):
        item = {'name': name}
        todos.append(item)
        return item

    def delete(self, name):
        for i, item in enumerate(todos):
            if item['name'] == name:
                todos.pop(i)
                return {'note': 'delete successful'}


class Todos(Resource):

    @staticmethod
    def get():
        return {'todos': todos}


api.add_resource(TodoItem, '/todo/<string:name>')
api.add_resource(Todos, '/todos')

if __name__ == '__main__':
    app.run()
