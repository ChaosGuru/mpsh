import os

from flask import Flask

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '3ECNQ1ReLA5sfmq7QHNGFkRDfvLxkS81')
app.config['JSON_AS_ASCII'] = False


from mpsh.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import mpsh.views
