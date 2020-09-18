from flask_restful import Resource
from sqlalchemy.orm import load_only

from models.article import Channel


class AllChannelResourse(Resource):
    '''所有频道'''
    def get(self):
        # 查询所有频道
        channels = Channel.query.options(load_only(Channel.id, Channel.name)).all()
        channels = [channel.to_dict() for channel in channels]
        return {'channels':channels}
