from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3307/auth"
    JWT_SECRET_KEY = "Mala_tajna"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
