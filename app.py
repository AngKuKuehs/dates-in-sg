"""
Loads the app.
"""

import os
import json

from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, request
from bson import json_util, ObjectId


app = Flask(__name__)

load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]
client = MongoClient(MONGODB_URI)

@app.route('/', methods=['GET'])
def default_route():
    """
    Returns a string
    """
    return 'Landing page for to-do-list project'

@app.route('/get-all', methods=['GET'])
def get_all_reminders():
    """Gets all date entries.

    Returns
    -------
    dict
        Details of all date entries.
    """
    db = client.todolist
    reminders_collection = db.reminders_test
    cursor = reminders_collection.find()
    result = []
    for document in cursor:
        document_cleaned = json.loads(json_util.dumps(document))
        result.append(document_cleaned)
    return result

@app.route('/get-one', methods=['GET'])
def get_one_reminder():
    """Gets a date entry.

    Query Parameter
    ----------
    oid: str
        date entry _id

    Returns
    -------
    dict
        Details of date entry.
    """
    oid = request.args.get('oid')
    db = client.todolist
    reminders_collection = db.reminders_test
    document_to_find = {"_id": ObjectId(oid)}
    result = reminders_collection.find_one(document_to_find)
    return json.loads(json_util.dumps(result))

@app.route('/add', methods=['POST'])
def add_reminder():
    """Adds a date entry.

    Request Body
    ----------
    application/json
        JSON object with date entry fields:
            "title": str
            "completed": bool

    Returns
    -------
    str
        Number of documents inserted.
    """
    db = client.todolist
    reminders_collection = db.reminders_test
    new_reminder = request.get_json()
    new_reminder = dict(new_reminder)

    if "title" in new_reminder and "completed" in new_reminder:
        result = reminders_collection.insert_one(new_reminder)
        return f"_id of inserted document: {result.inserted_id}"
    return "missing \"title\" or \"completed\""

@app.route('/update', methods=['PUT'])
def edit_reminder():
    """Updates a date entry.

    Query Parameters
    ----------
    oid: str
        id_ of date entry to update.

    Request Body
    ----------
    application/json
        JSON object with fields (keys) to update and corresponding update values.

    Returns
    -------
    str
        Number of documents updated.
    """
    db = client.todolist
    reminders_collection = db.reminders_test
    oid = request.args.get('oid')

    reminder_to_update = {"_id": ObjectId(oid)}
    updates = request.get_json()

    result = reminders_collection.update_one(reminder_to_update, {"$set": updates})

    return f"Documents updated: {str(result.modified_count)}"

@app.route('/remove', methods=['DELETE'])
def remove_reminder():
    """Deletes a date entry.

    Query Parameters
    ----------
    oid: str
        id_ of date entry to delete.

    Returns
    -------
    str
        Number of documents deleted.
    """
    db = client.todolist
    reminders_collection = db.reminders_test
    oid = request.args.get('oid')
    document_to_delete = {"_id": ObjectId(oid)}

    result = reminders_collection.delete_one(document_to_delete)
    return f"Documents deleted: {str(result.deleted_count)}"


if __name__ == "__main__":
    app.run()
