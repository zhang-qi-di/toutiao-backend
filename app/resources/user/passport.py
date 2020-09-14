import random
from datetime import datetime, timedelta

from flask_restful import Resource
from flask_restful.inputs import regex
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import redis_client
from models import db
from models.user import User
from utils.constants import SMS_CODE_EXPIRE, JWT_DAY_EXPIRE
from utils.parser import mobile as mobile_type

class SMSCodeResource(Resource):
    '''短信验证码'''
    def get(self,mobile):
        # 生成验证码
        # code = "%06d" % random.randint(0, 999999)
        code = '123456'
        # 将手机号和验证码保存到redis中     app:code:187xxx     123456
        redis_client.set('app:code:{}'.format(mobile),code,ex=SMS_CODE_EXPIRE)
        # 发送短信  celery发送异步任务
        print('发送短信：{mobile: %s,code: %s}' % (mobile,code))
        # 返回结果
        return {'mobile':mobile}

class LoginResource(Resource):
    '''用户登录'''
    def post(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('mobile',required=True,location='json',type=mobile_type)
        parser.add_argument('code',required=True,location='json',type=regex(r'\d{6}'))
        args = parser.parse_args()
        mobile = args.mobile
        code = args.code

        # 校验短信验证码
        key = 'app:code:{}'.format(mobile)
        real_code = redis_client.get(key)
        if not real_code or real_code != code:  # 验证失败
            return {'message':'Invalid Code'},400

        # 删除验证码
        # redis_client.delete(key)

        # 校验成功后，查询数据库中的用户数据
        user = User.query.options(load_only(User.id)).filter_by(mobile=mobile).first()
        if user:    # 如果有，进行登录，更新数据
            user.last_login = datetime.now()
        else:
            # 如果没有，进行注册，新增数据
            user = User(mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)

        db.session.commit()

        # 生成jwt
        from utils.jwt_util import generate_jwt
        token = generate_jwt({'userid':user.id}, expiry=datetime.utcnow() + timedelta(days=JWT_DAY_EXPIRE))

        # 返回数据
        return {'token':token},201















