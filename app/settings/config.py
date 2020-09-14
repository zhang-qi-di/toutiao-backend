class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/toutiao'   #数据库地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追究数据库变化
    SQLALCHEMY_ECHO = False     # 是否打印底层SQL语句

    REDIS_HOST = '127.0.0.1'    # redis的ip
    REDIS_PORT = 6381   # redis的端口

    JWT_SECRET = 'rh0LiNdhTIovxRVDiMJWhoaemKpCQOfN28N+TXQR'     # JWT秘钥


config_dict = {
    'dev':DefaultConfig
}