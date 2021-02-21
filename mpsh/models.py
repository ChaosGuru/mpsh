from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from mpsh.database import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    admin = Column(Boolean, default=False)
    task_completion = relationship("TaskCompletion")

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User %r>" % (self.name)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    points = Column(Integer, nullable=False)
    description = Column(Text)
    task_completion = relationship("TaskCompletion")

    def __init__(self, name, points, description=None):
        self.name = name
        self.points = points
        self.description = description

    def __repr__(self):
        return "<Task %r>" % (self.name)


class TaskCompletion(Base):
    __tablename__ = "completion"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))

    def __init__(self, team_id, task_id):
        self.team_id = team_id
        self.task_id = task_id


class MagicLink(Base):
    __tablename__ = "magic_links"
    id = Column(Integer, primary_key=True)
    email = Column(String(120))
    token_hash = Column(String(128))
    visits = Column(Integer, default=0)

    def __init__(self, email, token):
        self.email = email
        self.token_hash = generate_password_hash(token)

    def get_email(self, token):
        if check_password_hash(self.token_hash, token):
            self.visits += 1
            return self.email

        return None
