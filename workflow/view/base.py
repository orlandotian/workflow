from flask import Blueprint, url_for, render_template, request, flash, redirect, jsonify
from flask_login import logout_user, login_user, login_required, current_user
from workflow import app, db
from workflow import lgm
from workflow.model.model import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from workflow.util import util

bp = Blueprint('base', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index.html')


@lgm.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user


@lgm.unauthorized_handler
def unauthorized():
    flash('需要登录')
    url = request.path
    return redirect(url_for('base.login', next=url))


@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')


class LoginForm(FlaskForm):
    mobile = StringField('手机号', validators=[DataRequired('必填'), Length(max=11, min=11, message='必须是手机号')])
    pwd = PasswordField('密码', validators=[DataRequired('必填')])
    submit = SubmitField('登录')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mobile=form.mobile.data).first()
        if not user:
            flash('用户不存在')
            return render_template('login.html', form=form)
        if user.pwd != util.md5(form.pwd.data):
            flash('密码不正确')
            return render_template('login.html', form=form)
        if user.state == 1:
            flash('该用户被封停')
            return render_template('login.html', form=form)
        login_user(user)
        url = request.args.get('next')
        url = url if url else '/'
        return redirect(url)

    return render_template('login.html', form=form)


@bp.route('/currentUser')
@login_required
def get_user():
    return jsonify(current_user.to_json())


@bp.route('/myMembers')
@login_required
def get_members():
    group_id = current_user.group_id
    groups = User.query.filter(User.group_id == group_id).filter(User.id != current_user.id).all()
    results = [i.to_json() for i in groups]
    me = current_user.to_json()
    me['real_name'] = '我'
    results.insert(0, me)
    return jsonify(results)
