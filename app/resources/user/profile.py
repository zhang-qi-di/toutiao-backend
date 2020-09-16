from flask import g
from flask_restful import Resource
from sqlalchemy.orm import load_only

from models.user import User
from utils.decorators import login_required


class CurrentUserResource(Resource):
    '''个人中心-当前用户'''
    method_decorators = [login_required]

    def get(self):
        # 根据g中的user_id查询用户数据
        user = User.query.options(load_only(User.id,User.name,User.profile_photo,User.introduction,User.article_count,User.following_count,User.fans_count)).get(g.userid)

        # 返回数据
        return user.to_dict()