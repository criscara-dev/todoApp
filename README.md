# To do App in Flask with Okta

- create a to-do CRUD Rest (Representation State Transfer) API
  - create requests file: requests.http
  - my way to implement REST in Flank:
    - import Flask-RESTful package
  - create app full-stack in memory list:
    - convert GET, POST and DELETE methods via `SQLAlchemy` to get Objects from a real DB, create a Model
    - import Flask-SQLAlchemy and Flask-Migrate
    ```python
    app.config['SECRET_KEY'] = 'mysecretkey'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
    ```
    - create and import a Model
    - register a model using a migration `flask db init` and then run `flask db migrate "first migration"` it will add the sqlite file;  and finally `flask db upgrade`
- protect Rest API with OKTA Access token/Bearer token
  - secure API initially with JWT token... then add OKTA one;
  - authentication page -> username+password -> key -> key+request call -> etc.
    - install Flask-JWT-extended and basic usage code in app.py with imports
    - finally add decorator to API calls to protect API with Authentication @jwt_required
- switch list db to sqlite db
- vanilla frontend
- add OKTA sign-in

## How to run the App



## Signin users:
[Redirect authentication](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/asp-net-core-3/main/)

## Task to complete
- adding DB support
- [Protect your API endpoints](https://developer.okta.com/docs/guides/protect-your-api/aspnetcore3/main/)
- [Implement the OAuth 2.0 Authorization Code with PKCE Flow](https://developer.okta.com/blog/2019/08/22/okta-authjs-pkce)

## References:

[Build a Simple CRUD App with Flask and Python](https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python)

