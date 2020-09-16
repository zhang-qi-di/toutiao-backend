from flask import request, g

from utils.jwt_util import verify_jwt


def get_userinfo():
    '''获取用户身份信息'''
    # 提取请求头传递的token
    header = request.headers.get('Authorization')
    g.userid = None
    if header and header.startswith('Bearer'):
        token = header[7:]
        # 校验token
        payload = verify_jwt(token)
        if payload:
            g.userid = payload.get('userid')


