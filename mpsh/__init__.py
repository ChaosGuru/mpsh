from flask import Flask

app = Flask(__name__)


from mpsh.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def index():
    return "Hello, World"