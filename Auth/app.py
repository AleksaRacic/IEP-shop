from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager
from views import auth_view
from models import database


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_view)
jwt = JWTManager(app)

if __name__ == "__main__":
    database.init_app(app)
    app.run(debug=True, port=5000)
