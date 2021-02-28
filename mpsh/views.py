import functools
from uuid import uuid4

from flask import session, redirect, url_for, request, render_template, jsonify

from mpsh import app
from mpsh.database import db_session
from mpsh.models import User, QuestTask, QuestPoll, QuestCompletion, MagicLink


def login_required(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        if session['admin']:
            return view(**kwargs)
        elif session['user']:
            # get from kwargs url and check if the same
            return view(**kwargs)
        else:
            return redirect(url_for('index'))

    return wrapper


def admin_required(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        if not session['admin']:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapper


@app.route("/magic/<string:email>/<string:token>")
def magic(email, token):
    if MagicLink.valid_token(email, token):
        user = User.query.filter_by(email=email).first()

        if not user:
            user = User('new_user', email)

        if user.admin:
            session['admin'] = True
        
        session['user'] = user.id

    return redirect(url_for('index'))


@app.route("/create-magic")
def create_magic(): 
    users = User.query.all()
    magic = {}
    
    for user in users:
        token = str(uuid4())
        old_m = MagicLink.query.filter_by(email=user.email).first()

        if old_m:
            db_session.delete(old_m)
            db_session.commit()

        new_m = MagicLink(user.email, token)
        db_session.add(new_m)
        db_session.commit()

        magic[user.email] = url_for('magic', 
                                    email=user.email, 
                                    token=token, 
                                    _external=True)

    return jsonify(magic)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/ranks")
def ranks():
    # take data from database

    return render_template('ranks.html')


@app.route("/tasks/<string:team>")
def tasks(team):
    # take data from database

    # check if team is the same as in url

    return render_template('tasks.html')


@app.route("/admin")
@admin_required
def admin():


    return render_template('admin.html')