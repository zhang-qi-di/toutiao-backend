from flask import Blueprint
from flask_restful import Api
from app.resources.user.passport import SMSCodeResource

# 创建蓝图对象

user_bp = Blueprint('user', __name__)

# 创建api对象
user_api = Api(user_bp)

# 添加类视图
user_api.add_resource(SMSCodeResource,'/sms/codes')