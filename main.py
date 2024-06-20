from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from config import connection_string, JWT_SECRET_KEY
from flask_jwt_extended import JWTManager, create_access_token

load_dotenv(find_dotenv())

client = MongoClient(connection_string)
habit_tracker = client["habit_tracker"]

def create_app():
    app = Flask(__name__)
    jwt = JWTManager(app)
    app.config["habits_collection"] = habit_tracker["habits"]
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    from routes import register_routes
    register_routes(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)