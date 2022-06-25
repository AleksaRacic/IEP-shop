from flask import Flask
from flask_jwt_extended import JWTManager
from views import warehouse_view
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(warehouse_view)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
