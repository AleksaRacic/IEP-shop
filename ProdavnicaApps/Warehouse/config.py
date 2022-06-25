import os;

redis_host = os.environ["REDIS_HOST"]

class Config:
    REDIS_HOST = redis_host
    REDIS_THREADS_LIST = "Proizvodi"
    JWT_SECRET_KEY = "Mala_tajna"
