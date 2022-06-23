from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import Config
from models import database
from sqlalchemy_utils import database_exists, create_database

application: Flask = Flask(__name__)
application.config.from_object(Config)

migrate = Migrate(application, database)

manager = Manager(application)
manager.add_command("db", MigrateCommand)

if (__name__ == '__main__'):
    database.init_app(application)
    if (not database_exists(Config.SQLALCHEMY_DATABASE_URI)):
        create_database(Config.SQLALCHEMY_DATABASE_URI)
        #TODO dodati admina i role, radio je u nekom od videa
    manager.run()
