from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from mpsh.database import Base, db_session
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    admin = Column(Boolean, default=False)

    task_completion = relationship("QuestCompletion")

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User %r>" % (self.name)


class QuestTask(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    legend = Column(Text, nullable=False)
    max_points = Column(Integer, nullable=False)
    poll_id = Column(Integer, ForeignKey('polls.id'))

    polls = relationship("QuestPoll", back_populates="tasks")
    completion = relationship("QuestCompletion")

    def __init__(self, name, max_points, legend, poll_id):
        self.name = name
        self.max_points = max_points
        self.legend = legend
        self.poll_id = poll_id

    def __repr__(self):
        return "<Task %r>" % (self.name)


class QuestPoll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(String(100), nullable=False)

    tasks = relationship("QuestTask", uselist=False, back_populates="polls")

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return "<Poll %r>" % (self.question)


class QuestCompletion(Base):
    __tablename__ = "completion"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    points = Column(Integer, nullable=False)
    solved_question = Column(Boolean, default=False)

    def __init__(self, team_id, task_id, points):
        self.team_id = team_id
        self.task_id = task_id
        self.points = points

    @staticmethod
    def team_score(team_id):
        score = 0
        objs = QuestCompletion.query.filter_by(team_id=team_id).all()

        for obj in objs:
            score += obj.points

            if obj.solved_question:
                score += 20

        return score

    @staticmethod
    def solve_question(team_id, answer):
        obj = QuestCompletion.query.filter_by(team_id=team_id).first()
        task = QuestTask.query.filter_by(id=obj.task_id).first()
        quest = QuestPoll.query.filter_by(id=task.poll_id).first()

        if quest.answer == answer:
            obj.solved_question = True
            db_session.commit()

            return True
        else:
            return False

    @staticmethod
    def complete_task(team_id, task_id, points):
        obj = QuestCompletion.query.filter_by(team_id=team_id).first()
        task = QuestTask.query.filter_by(task_id=task_id).first()
        points = min(points, task.max_points)

        if not obj:
            new_obj = QuestCompletion(team_id, task_id, points)
            db_session.add(new_obj)
        else:
            obj.points = points

        db_session.commit()



class MagicLink(Base):
    __tablename__ = "magic_links"
    id = Column(Integer, primary_key=True)
    email = Column(String(120))
    token_hash = Column(String(128))
    visits = Column(Integer, default=0)

    def __init__(self, email, token):
        self.email = email
        self.token_hash = generate_password_hash(token)

    @staticmethod
    def valid_token(email, token):
        obj = MagicLink.query.filter_by(email=email).first()

        if obj:
            obj.visits += 1
            db_session.commit()
            return True

        return False
