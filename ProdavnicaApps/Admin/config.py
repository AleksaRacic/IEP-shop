import os;

databaseUrl = os.environ["DATABASE_URL"]

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/prodavnica"
    JWT_SECRET_KEY = "Mala_tajna"
