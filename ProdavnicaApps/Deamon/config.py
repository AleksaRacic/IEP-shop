import os

databaseUrl = os.environ["DATABASE_URL"]
redis_host = os.environ["REDIS_HOST"]

class Config:
    REDIS_HOST = redis_host
    REDIS_THREADS_LIST = "Proizvodi"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/prodavnica"
    JWT_SECRET_KEY = "Mala_tajna"
