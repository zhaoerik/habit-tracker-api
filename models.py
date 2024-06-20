from bson.objectid import ObjectId
from datetime import datetime

def get_all_habits(habits_collection):
    habits = habits_collection.find() 
    return list(habits)

def query_habit_by_id(habits_collection, habit_id=None):
    try:
        query = {}
        _id = ObjectId(habit_id)
        query["_id"]= _id
        return habits_collection.find_one(query)
    except Exception as e:
        print(f"Error querying habits: {e}")

def create_habit_doc(habits_collection, _name, _description):
    if habits_collection.find_one({"name": _name}):
        print(f"habit '{_name}' already exists")
        return False
    else:
        today = datetime.today()
        new_habit_doc = {
            "name": _name,
            "description": _description,
            "frequency": 0,
            "start_date": today,
            "last_date": today
        }
        return habits_collection.insert_one(new_habit_doc).inserted_id

def update_habit(habits_collection, habit_id, updated_habit_data):
    filter = {"_id": ObjectId(habit_id)}
    updated_values = {"$set": {}}
    try:
        for key, value in updated_habit_data.items():
            if value != "":
                updated_values["$set"][key] = value
            if key == "frequency" and value == "":
                updated_values["$set"][key] = 0
        
        # update last date
        updated_values["$set"]["last_date"] = datetime.today()

        habits_collection.update_one(filter, updated_values)

        updated_habit = habits_collection.find_one(filter)
        return updated_habit

    except Exception as e:
        print(f"Error updating habit: {e}")

def delete_habit(habits_collection, habit_id):
    try:
        query = {}
        query["_id"] = ObjectId(habit_id)
        habits_collection.delete_one(query)

    except Exception as e:
        print(f"Error deleting habit: {e}")