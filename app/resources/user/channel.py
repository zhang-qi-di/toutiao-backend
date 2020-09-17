from flask import g
from flask_restful import Resource
from sqlalchemy.orm import load_only

from models.article import Channel, UserChannel


class UserChannelResource(Resource):
    '''用户频道'''

    def get(self):
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











