from workflow import app
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from workflow.model.model import Group, Department, User, Task
from workflow import db


def is_accessible():
    user = current_user
    return current_user.is_authenticated and user.real_name == 'admin'


class MyIndexAdminView(AdminIndexView):
    name = '主页'
    url = '/admin'
    template = 'admin/index.html'


class CommonModelView(ModelView):

    def is_accessible(self):
        return is_accessible()


class OtherModelView(CommonModelView):
    column_filters = ('shop_id','username')
    column_searchable_list = ('shop_id', 'username')


admin = Admin(app, name='工作流', template_mode='bootstrap3', index_view=MyIndexAdminView())
admin.add_view(CommonModelView(Department, db.session, name='部门管理', endpoint='adepart'))
admin.add_view(CommonModelView(Group, db.session, name='分组管理', endpoint='agroup'))
admin.add_view(CommonModelView(User, db.session, name='用户管理', endpoint='auser'))
admin.add_view(CommonModelView(Task, db.session, name='任务管理', endpoint='atask'))
