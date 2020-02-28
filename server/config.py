from datetime import datetime, timedelta

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:2016Unitec@localhost/schedule?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=8)