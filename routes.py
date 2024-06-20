from flask import request, jsonify
from models import get_all_habits, query_habit_by_id, create_habit_doc, update_habit, delete_habit
from config import parse_json
from flask_jwt_extended import jwt_required, create_access_token

def register_routes(app):
    @app.route("/login", methods=["POST"])
    def login():
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if username != "test" or password != "test":
            return jsonify({"message": "Bad username or password"}), 401
    
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    
    @app.route("/", methods=["GET"])
    @jwt_required()
    def home():
        return "Habit Tracker API"

    @app.route("/habits", methods=["GET"])
    @jwt_required()
    def api_get_habits():
        try:
            habits = get_all_habits(app.config["habits_collection"])
        except Exception as e:
            return jsonify({"error": str(e)})
        return parse_json(habits), 200

    @app.route("/habits/<id>", methods=["GET"])
    @jwt_required()
    def api_get_habit(id):
        habit = query_habit_by_id(app.config["habits_collection"], id)
        if habit is None:
            return jsonify({"error": "Habit not found"}), 404

        return parse_json(habit), 200

    @app.route("/habit", methods=["POST"])
    @jwt_required()
    def api_create_habit():
        post_data = request.get_json()
        try:
            new_habit_id = create_habit_doc(app.config["habits_collection"], post_data["name"], post_data["description"])
            if not new_habit_id:
                error_response = {"error": "Habit with that name already exists"}
                return jsonify(error_response), 400
            else:
                return jsonify({"message": "Habit created successfully", "habit": api_get_habit(new_habit_id)}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route("/habits/<id>", methods=["PUT"])
    @jwt_required()
    def api_update_habit(id):
        post_data = request.get_json()
        try:
            updated_habit_data = {
                "name": post_data["name"], 
                "description": post_data["description"], 
                "frequency": post_data["frequency"]
            }
            updated_habit = update_habit(app.config["habits_collection"], id, updated_habit_data)
            return parse_json(updated_habit), 200

        except Exception as e:
            return jsonify({"error": str(e)})

    @app.route("/habits/<id>", methods=["DELETE"])
    @jwt_required()
    def api_delete_habit(id):
        habit = query_habit_by_id(app.config["habits_collection"], id)

        if habit is None:
            return jsonify({"error": "Habit not found"}), 404
        
        delete_habit(app.config["habits_collection"], id)
        response = {"message": "Habit deleted successfully"}
        return jsonify(response), 200