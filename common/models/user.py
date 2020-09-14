from . import db


class User(db.Model):
    """
    用户基本信息
    """
    __tablename__ = 'user_basic'

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    name = db.Column('user_name', db.String, doc='昵称')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    introduction = db.Column(db.String, doc='简介')
    article_count = db.Column(db.Integer, default=0, doc='作品数')
    following_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='粉丝数')
    profile_photo = db.Column(db.String, doc='头像')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'photo': self.profile_photo,
            'intro': self.introduction,
            'art_count': self.article_count,
            'follow_count': self.following_count,
            'fans_count': self.fans_count
        }
