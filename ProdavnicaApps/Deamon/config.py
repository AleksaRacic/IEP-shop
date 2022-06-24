from datetime import timedelta

class Config:
    REDIS_HOST = "localhost"
    REDIS_THREADS_LIST = "Proizvodi"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3308/prodavnica"
    JWT_SECRET_KEY = "Mala_tajna"
