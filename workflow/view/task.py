from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from workflow.model.model import Task
from workflow import db, socketio
from datetime import datetime, timedelta
from flask_socketio import emit

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('', methods=['POST'])
@login_required
def view_task():
    year = request.json.get('year')
    month = request.json.get('month')
    uid = request.json.get('uid')
    if not uid:
        uid = []
        uid.append(current_user.id)

    startMonth = datetime.strptime('%s-%s-1'%(year, month), '%Y-%m-%d')
    endMonth = startMonth + timedelta(days=31)
    tasks = Task.query.filter(Task.add_time.between(startMonth, endMonth)).filter(Task.user_id.in_(uid)).order_by(Task.state.desc(), Task.id.desc()).all()
    result = {}
    for t in tasks:
        t_json = t.to_json()
        if not result.get(t_json['time_str']):
            result[t_json['time_str']] = []
        result[t_json['time_str']].append(t_json)

    return jsonify(result)


@bp.route('/add', methods=['POST'])
@login_required
def add_task():
    newTask = request.json.get('newTask')
    addTime = request.json.get('addTime')
    if newTask and addTime:
        task = Task()
        task.user_id = current_user.id
        task.name = newTask
        task.add_time = datetime.strptime(addTime, '%Y/%m/%d')
        db.session.add(task)
        db.session.commit()
        event_message({'msg':'%s添加了新任务<%s>'%(current_user.real_name, task.name)})
    return jsonify([])


@bp.route('/updateState', methods=['POST'])
@login_required
def update_state():
    task_id = request.json.get('id')
    if id:
        task = Task.query.filter(Task.id == int(task_id)).first()
        if task:
            if task.state == 0:
                task.state = 1
                task.end_time = datetime.now()
                task.update_time = datetime.now()
            elif task.state == 1:
                task.state = 0
                task.update_time = datetime.now()
                task.end_time = None
            db.session.add(task)
        return jsonify(task.to_json())
    return jsonify(None)


@socketio.on('event_update')
def event_update(json):
    emit('response_update', json, broadcast=True, namespace='')


@socketio.on('event_message')
def event_message(json):
    emit('response_message', json, broadcast=True, namespace='')


