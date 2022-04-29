import os.path
from flask import Flask, render_template, request, redirect, url_for, g
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_oidc import OpenIDConnect
from okta import UsersClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

##########################
##### SQL DATABASE #######
##########################


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
# instantiate SQLAlchemy
db = SQLAlchemy(app)
Migrate(app, db)

##########################
##### OKTA SETUP  #######
##########################


app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config['SECRET_KEY'] = '\xffI\x18M\x977\x19,\xd2|\x7f\xbc\xf6J\xc4%'
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
okta_client = UsersClient("{{ OKTA_ORG_URL }}", "{{ OKTA_AUTH_TOKEN }}")

api = Api(app, prefix="/api/v1")


##########################
##### VIEW FUNCTONS ######
##########################


@app.route('/', methods=['GET', 'POST'])
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/api/v1/todos', methods=['GET', 'POST'])
@oidc.require_login
def get_todos():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/api/v1/todo', methods=['POST'])
@oidc.require_login
def add():
    todo = Todo(name=request.form['todoitem'])
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/api/v1/todo/delete/<string:name>')
@oidc.require_login
def delete(name):
    item = Todo.query.filter_by(name=name).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


@app.route("/userprofile")
def userprofile():
    return render_template("userprofile.html")


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for("index"))


@app.errorhandler(403)
def insufficient_permissions(e):
    """Render a 403 page."""
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


##########################
######## MODELS ##########
##########################


class Todo(db.Model):
    name = db.Column(db.String(20), primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'The task name is: {self.name}'

    # def json(self):
    #     return {'name': self.name}


class TodoItem(Resource):

    @staticmethod
    def post(name):
        item = Todo(name=name)
        db.session.add(item)
        db.session.commit()

        return item.json()

    @staticmethod
    def delete(name):
        item = Todo.query.filter_by(name=name).first()
        db.session.delete(item)
        db.session.commit()
        return {'note': 'delete successful'}


class Todos(Resource):
    def get(self):
        todos = Todo.query.all()
        return [item.json() for item in todos]


# The following resources are now accessible to our API
api.add_resource(TodoItem, '/todo/<string:name>')
api.add_resource(Todos, '/todos')

if __name__ == '__main__':
    app.run()
