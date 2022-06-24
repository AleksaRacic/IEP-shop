from flask import Flask
from flask_jwt_extended import JWTManager
from views import warehouse_view

app = Flask(__name__)
app.register_blueprint(warehouse_view)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
