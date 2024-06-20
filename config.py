from dotenv import load_dotenv, find_dotenv
import os
import json

load_dotenv(find_dotenv())

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
username = os.environ.get("MONGO_USERNAME")
password = os.environ.get("MONGO_PWD")
connection_string = f"mongodb+srv://{username}:{password}@dev-cluster.uasmcge.mongodb.net/?retryWrites=true&w=majority&appName=dev-cluster"

def parse_json(data):
    return json.loads(json.dumps(data, default=str))