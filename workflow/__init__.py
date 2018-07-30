from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_mapping(
    DEBUG=True,
    SECRET_KEY='dev',
    # SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'data.sqlite'),
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://test:zaq1xsw2@127.0.0.1:3306/workflow?charset=UTF8MB4',
#     SQLALCHEMY_DATABASE_URI='mysql+pymysql://memsys:Yyups1@114.215.143.65:3306/memsys?charset=UTF8MB4',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
)

db = SQLAlchemy(app)
lgm = LoginManager(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


from workflow.view import base, task

app.register_blueprint(base.bp)
app.register_blueprint(task.bp)

from workflow.view import admin

from workflow.model.model import User


def init_admin():
    shop = User.query.filter_by(real_name='admin').first()
    if shop:
        return
    admin = User()
    admin.mobile = '18518461858'
    admin.real_name = 'admin'
    admin.pwd = 'zaq1xsw2'
    db.session.add(admin)
    db.session.commit()


# db.drop_all()
db.create_all()
init_admin()
