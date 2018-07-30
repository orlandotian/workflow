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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    real_name = db.Column(db.String(50))
    mobile = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(50), default='000000')
    this_login = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime, default=datetime.now())
    state = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.real_name

    def to_json(self):
        return {
            'id': self.id,
            'real_name': self.real_name,
            'mobile': self.mobile,
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='tasks')
    name = db.Column(db.String(100))
    priority = db.Column(db.Integer, default=0)
    state = db.Column(db.Integer, default=0)
    add_time = db.Column(db.DateTime, default=datetime.now())
    expected_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, default=datetime.now())
    end_time = db.Column(db.DateTime)

    def __repr__(self):
        return self.name[:10]

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user': self.user.real_name,
            'user_id': self.user.id,
            'priority': self.priority,
            'state': self.state,
            'add_time': self.add_time,
            'time_str': self.add_time.strftime('%Y/%m/%d')
        }
