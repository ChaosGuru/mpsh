from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from mpsh.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    admin = Column(Boolean, default=False)
    # for what I need this??
    task_completion = relationship("TaskCompletion")

    def __init__(self, name, email)
        self.name = names
        self.email = email

    def __repr__(self):
        return "<User %r>" % (self.name)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    points = Column(Integer, nullable=False)
    description = Column(Text)
    # for what I need this??
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
