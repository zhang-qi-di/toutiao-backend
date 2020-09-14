from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import *
import sys

# 添加common路径到模块查询路径中
BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0,BASE_DIR + '/common')

from app.settings.config import config_dict
from utils.constants import EXTRA_ENV_CONFIG
from redis import StrictRedis


# 创建redis客户端
redis_client = None     # type:StrictRedis


def create_flask_app(config_type):
    '''创建Flask应用'''
    # 创建应用
    app = Flask(__name__)

    # 根据配置类型选择配置子类
    config_class = config_dict[config_type]
    # 先加载默认配置
    app.config.from_object(config_class)
    # 再加载额外配置
    app.config.from_envvar(EXTRA_ENV_CONFIG,silent=True)

    # 返回应用
    return app

def register_extensions(app):
    '''注册组件'''
    # 初始化数据库组件
    from models import db
    db.init_app(app)    # 第二种初始化方式
    # 初始化redis
    global redis_client
    redis_client = StrictRedis(host=app.config['REDIS_HOST'],port=app.config['REDIS_PORT'],decode_responses=True)

def register_blueprint(app:Flask):
    '''注册蓝图对象'''
    from app.resources.user import user_bp
    app.register_blueprint(user_bp)

def create_app(config_type):
    '''应用初始化'''
    # 创建Flask应用
    app = create_flask_app(config_type)
    # 初始化组件
    register_extensions(app)

    # 注册转换器
    from utils.converters import register_converters
    register_converters(app)

    # 注册蓝图
    register_blueprint(app)
    return app















