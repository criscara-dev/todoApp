import os.path

from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

api = Api(app, prefix="/api/v1")

# list (of dictionaries) as in memory db
todos = [
    # {"name": "this is my first task"}
]


@app.route('/')
def index():  # put application's code here
    return 'Welcome!'


class Todo(db.Model):
    name = db.Column(db.String(80), primary_key=True)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name}


class TodoItem(Resource):

    # @staticmethod
    # def post(name):
    #     item = {'name': name}
    #     todos.append(item)
    #     return item

    # db method
    @staticmethod
    def post(name):
        item = Todo(name=name)
        db.session.add(item)
        db.session.commit()

        return item.json()

    # @staticmethod
    # def delete(name):
    #     for i, item in enumerate(todos):
    #         if item['name'] == name:
    #             todos.pop(i)
    #             return {'note': 'delete successful'}

    # db method
    @staticmethod
    def delete(name):
        item = Todo.query.filter_by(name=name).first()
        db.session.delete(item)
        db.session.commit()
        return {'note': 'delete successful'}


class Todos(Resource):

    # def get(self):
    #     return {'todos': todos}

    # db method
    def get(self):
        todos = Todo.query.all()
        return [item.json() for item in todos]


api.add_resource(TodoItem, '/todo/<string:name>')
api.add_resource(Todos, '/todos')

if __name__ == '__main__':
    app.run()
