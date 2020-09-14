from flask import Blueprint
from flask_restful import Api
from app.resources.user.passport import SMSCodeResource
from utils.constants import BASE_URL_PREFIX


# 创建蓝图对象

user_bp = Blueprint('user', __name__,url_prefix=BASE_URL_PREFIX)

# 创建api对象
user_api = Api(user_bp)

# 添加json外层包装
from utils.output import output_json
user_api.representation('application/json')(output_json)

# 添加类视图
user_api.add_resource(SMSCodeResource,'/sms/codes/<mob:mobile>')

