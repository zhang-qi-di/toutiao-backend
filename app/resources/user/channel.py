from flask import g, request
from flask_restful import Resource
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import load_only

from models import db
from models.article import Channel, UserChannel
from utils.decorators import login_required


class UserChannelResource(Resource):
    '''用户频道'''

    method_decorators = {'put':[login_required]}

    def get(self):
        '''获取用户频道'''
        userid = g.userid

        if userid:  # 用户已登录，查询用户频道
            # 获取用户关注的所有频道数据
            channels = Channel.query.options(load_only(Channel.id,Channel.name)).\
                join(UserChannel,Channel.id == UserChannel.channel_id).\
                filter(UserChannel.user_id == userid,UserChannel.is_deleted == False).\
                order_by(UserChannel.sequence).all()

            if len(channels) == 0:  # 如果用户没有选择过频道，查询默认频道列表
                channels = Channel.query.options(load_only(Channel.id,Channel.name)).filter(
                    Channel.is_default == True).all()

        else:   # 用户未登录，查询默认频道列表
            channels = Channel.query.options(load_only(Channel.id, Channel.name)).filter(
                Channel.is_default == True).all()

        # 序列化
        channel_list = [channel.to_dict() for channel in channels]

        # 插入"推荐"频道(数据来源为推荐系统)
        channel_list.insert(0,{'id':0,'name':'推荐'})

        return {'channels':channel_list}

    def put(self):
        '''修改用户频道'''
        # 获取参数
        channels = request.json.get('channels')

        # 将数据库中原有的数据全部逻辑删除
        UserChannel.query.filter(UserChannel.is_deleted == False, UserChannel.user_id == g.userid).\
            update({'is_deleted':True})

        # 更新数据（重置式）
        for channel in channels:
            # 第一种情况  本来就关注了该频道，只是修改了顺序  -> 更新数据
            # 第二种情况  新关注的频道  -> 增加数据
            statement = insert(UserChannel).values(user_id=g.userid, channel_id=channel['id'],
                                                sequence=channel['seq']).on_duplicate_key_update(
                sequence=channel['seq'], is_deleted=False)

            db.session.execute(statement)

        db.session.commit()

        # 返回结果
        return {'channels':channels}


























