# To do App 

---

## Getting Started 🚀


### Description 📄
The application let you add and delete tasks from a data store inplemented in SQLite.
The server-side application has been integrated with Okta for authentication and tokens.
The REST API endpoints are protected via Okta decorator so, only available for users that have OIDC.

### Technologies used 🛠
Flask web framework for Python
SQLite DBMS
Flask OpenIDConnect
Okta SDK for Python

P.S.
I choose not to use the package for Flask WTF forms since I just have a simple form with 1 field.

### How To Setup the Project 🔧

- Install the requirements.txt via the CLI command: `pip install -r requirements.txt`
- To create the DB file (and to have the DB ready for changes in the Schema), run:
```python
flask db init
flask db migrate -m 'first migration'
flask db upgrade
```
- Get an Authorization token from an Identity and secure Access Management platform:
  - Sign-up to a developer account at Okta
  - Create an OIDC - OpenID Connect app
  - Get the Authorization token.
  - Create a new file named `client_secrets.json`  in the root of your project folder and insert the following code:
```python
{
  "web": {
    "client_id": "{{ OKTA_CLIENT_ID }}",
    "client_secret": "{{ OKTA_CLIENT_SECRET }}",
    "auth_uri": "{{ OKTA_ORG_URL }}/oauth2/default/v1/authorize",
    "token_uri": "{{ OKTA_ORG_URL }}/oauth2/default/v1/token",
    "issuer": "{{ OKTA_ORG_URL }}/oauth2/default",
    "userinfo_uri": "{{ OKTA_ORG_URL }}/oauth2/default/userinfo",
    "redirect_uris": [
      "http://localhost:5000/oidc/callback"
    ]
  }
}       
```
- replace the placeholder variables with your actual Okta information.
- In the `app.py` file, replace the placeholder variables with your Okta details:
```python
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "{{ LONG_RANDOM_STRING }}"
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
okta_client = UsersClient("{{ OKTA_ORG_URL }}", "{{ OKTA_AUTH_TOKEN }}")
```
---

### How To Run the Project 🎬

- On your Terminal CLI run:
```shell
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
# Running on http://127.0.0.1:5000/
```
---

## License 📄

This project is licensed under the MIT License - see the [LICENSE.md](https://choosealicense.com/licenses/mit/) file for details.

---

## Credits/References 🎁

- [Redirect authentication](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/asp-net-core-3/main/)
- [Build a Simple CRUD App with Flask and Python](https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python)
- [4-Python Flask - Okta Identity & Access Management by Paul Mahon](https://www.youtube.com/watch?v=A1u0iOakQpk&t=430s)
