from flask import Blueprint, url_for, render_template, request, flash, redirect, jsonify
from flask_login import logout_user, login_user, login_required
from workflow import app, db
from workflow import lgm
from workflow.model.model import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

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
        if user.pwd != form.pwd.data:
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