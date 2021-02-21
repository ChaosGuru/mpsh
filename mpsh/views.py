import functools

from flask import session, redirect, url_for, request, render_template

from mpsh import app


def login_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not session['user']:
            return redirect(url_for('index'))

        return view(*args, **kwargs)

    return wrapper


def admin_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not session['admin']:
            return redirect(url_for('index'))

        return view(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    session['admin'] = False
    session['user'] = 1
    return render_template('index.html')


@app.route("/ranks")
def ranks():
    # take data from databese

    return render_template('ranks.html')


@app.route("/tasks/<team>")
@login_required
def tasks(team):
    # take data from database

    # chech if team is the same as in url

    return render_template('tasks.html')


@app.route("/admin")
@admin_required
def admin():


    return render_template('admin.html')