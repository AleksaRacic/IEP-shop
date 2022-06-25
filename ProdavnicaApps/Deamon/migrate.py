from time import sleep

from flask import Flask
from config import Config
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database
from models import *

application = Flask(__name__)
application.config.from_object(Config)

migrateObject = Migrate(application, database)

done = False

while not done:
    try:
        if (not database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
            create_database(application.config["SQLALCHEMY_DATABASE_URI"])

        database.init_app(application)

        with application.app_context() as context:
            init()
            migrate(message="Production migration")
            upgrade()
        done = True
        print("Connected")
    except Exception as err:
        print(err)
        sleep(3)