from flask import Flask
from config import Config
from views import auth_view

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_view)
