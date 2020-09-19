from flask import Blueprint
from flask_restful import Api

from app.resources.article.channel import AllChannelResourse
from utils.constants import BASE_URL_PREFIX


# 创建蓝图对象

article_bp = Blueprint('article', __name__,url_prefix=BASE_URL_PREFIX)

# 创建api对象
article_api = Api(article_bp)

# 添加json外层包装
from utils.output import output_json
article_api.representation('application/json')(output_json)

# 添加类视图
article_api.add_resource(AllChannelResourse,'/channels')
