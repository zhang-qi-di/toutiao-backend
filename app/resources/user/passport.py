import random

from flask_restful import Resource

from app import redis_client
from utils.constants import SMS_CODE_EXPIRE


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

