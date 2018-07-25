from workflow import db
from flask_login import UserMixin
from datetime import datetime


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    groups = db.relationship('Group', backref='department', lazy='dynamic')

    def __repr__(self):
        return self.name


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    users = db.relationship('User', backref='group', lazy='dynamic')

    def __repr__(self):
        return self.name


user_task = db.Table('user_task',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    real_name = db.Column(db.String(50))
    mobile = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(50), default='000000')
    this_login = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime, default=datetime.now())
    state = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task', secondary=user_task, backref='users')

    def __repr__(self):
        return self.real_name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    priority = db.Column(db.Integer)
    state = db.Column(db.Integer, default=0)
    add_time = db.Column(db.DateTime, default=datetime.now())
    expected_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    end_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return self.name[:10]
