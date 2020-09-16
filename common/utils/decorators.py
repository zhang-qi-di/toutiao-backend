from flask import g, abort
from functools import wraps


def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if g.userid:    # 如果用户已登录，正常访问视图
            return f(*args, **kwargs)
        else:
            print('401')
            abort(401)

    return wrapper