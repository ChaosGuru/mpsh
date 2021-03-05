import functools
from uuid import uuid4
from difflib import SequenceMatcher

from flask import session, redirect, url_for, request, render_template, jsonify, flash

from mpsh import app
from mpsh.database import db_session
from mpsh.models import (User, QuestTask, Poll, PollCompletion, 
                         QuestCompletion, MagicLink)


def login_required(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        msg = "учасник команди"
        if session.get('admin', False):
            return view(**kwargs)
        elif session.get('user', False):
            # get from kwargs url and check if the same
            return view(**kwargs)
        else:
            return render_template('non-team.html', msg=msg)

    return wrapper


def admin_required(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        msg = "інструктор"
        if not session.get('admin', False):
            return render_template('non-team.html', msg=msg)

        return view(**kwargs)

    return wrapper


@app.route("/magic/<string:email>/<string:token>")
def magic(email, token):
    if MagicLink.valid_token(email, token):
        user = User.query.filter_by(email=email).first()

        if not user:
            user = User('new_user', email)

        session['admin'] = False
        if user.admin:
            session['admin'] = True
        
        session['user'] = user.id

    return redirect(url_for('index'))


@app.route("/create-magic")
@admin_required
def create_magic(): 
    users = User.query.all()
    magic = {}
    
    for user in users:
        token = str(uuid4())

        m = MagicLink(user.email, token)
        db_session.add(m)
        db_session.commit()

        magic[user.name] = url_for('magic', 
                                    email=user.email, 
                                    token=token, 
                                    _external=True)

    return jsonify(magic)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/ranks")
def ranks():
    get_score = lambda team_id: QuestCompletion.team_score(team_id)

    teams = User.query.filter_by(admin=False)
    scores = [(get_score(t.id), t.name, t.id) for t in teams]

    leaderboard = tuple(enumerate(sorted(scores, key=lambda x: x[0], reverse=True)))

    return render_template('ranks.html', leaderboard=leaderboard)


@app.route("/tasks/<int:team_id>")
@login_required
def tasks(team_id):
    tasks = QuestTask.query.all()
    complete = QuestCompletion.query.filter_by(team_id=team_id).all()
    complete_dict = {d.task_id:d for d in complete}
    team_name = User.query.filter_by(id=team_id).first().name
    
    tasks_num = len(tasks)
    ctasks_num = 0

    polls = Poll.query.all()
    cpolls = PollCompletion.query.filter_by(team_id=team_id).all()
    polls_num = len(polls)
    cpolls_num = len(cpolls)

    quest_tasks = []
    for task in tasks:
        qt = {}
        qt["name"] = task.name
        qt["max_points"] = task.max_points
        qt["legend"] = task.legend

        if task.id in complete_dict.keys():
            qt["points"] = complete_dict[task.id].points
            ctasks_num += 1
        else:
            qt["points"] = 0

        quest_tasks.append(qt)

    return render_template('tasks.html', 
                           tasks=quest_tasks, 
                           tasks_num=tasks_num, 
                           ctasks_num=ctasks_num,
                           polls_num=polls_num,
                           cpolls_num=cpolls_num,
                           team_name=team_name)


@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    if request.method == "POST":
        team_id = request.form["teams"]
        task_id = request.form["tasks"]
        points = int(request.form["points"])

        QuestCompletion.complete_task(team_id, task_id, points)

        return redirect(url_for('admin'))

    teams = User.query.filter_by(admin=False)
    tasks = QuestTask.query.all()
    polls = Poll.query.all()
    cpolls = PollCompletion.query.all()
    survey = {}

    for team in teams:
        survey[team.name] = []
        for poll in polls:
            answ = [poll.question, poll.answer, "Немає відповіді"]
            for cpoll in cpolls:
                if poll.id == cpoll.poll_id and team.id == cpoll.team_id:
                    answ[2] = cpoll.answer
                    break

            survey[team.name].append(answ)

    return render_template('admin.html', 
                           teams=teams, 
                           tasks=tasks, 
                           survey=survey)


@app.route("/poll/<int:poll_num>", methods=["GET", "POST"])
@login_required
def poll(poll_num):
    poll_id = poll_num // 71
    poll = Poll.query.filter_by(id=poll_id).first()

    if request.method == "POST":
        team_id = session['user']
        answer = request.form["answer"]
        
        if PollCompletion.query.filter_by(team_id=team_id, poll_id=poll_id).first():
            flash("Ви уже відповідали на це питання.")
            return render_template('poll.html', question=poll.question)

        p = PollCompletion(team_id, poll_id, answer)
        db_session.add(p)
        db_session.commit()

        flash("Ваша відповідь надіслана. Відповідь на це питання: %s." % (poll.answer))
    
    return render_template('poll.html', question=poll.question)


@app.route("/poll/links")
@admin_required
def poll_links():
    polls = Poll.query.all()
    links = []

    for poll in polls:
        l = url_for('poll', poll_num=poll.id * 71, _external=True)
        links.append(l)

    return jsonify(links)