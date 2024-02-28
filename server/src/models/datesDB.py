import os
import json
import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util, ObjectId

load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]
client = MongoClient(MONGODB_URI)

def models_ok():
    return "models ok"

def get_all_dates_from_db():
    db = client["dates-in-sg"]
    dates_collection = db.dates
    cursor = dates_collection.find()
    result = []
    for document in cursor:
        document_cleaned = json.loads(json_util.dumps(document))
        result.append(document_cleaned)
    return result

def get_one_date_from_db(oid):
    db = client["dates-in-sg"]
    dates_collection = db.dates
    document_to_find = {"_id": ObjectId(oid)}
    result = dates_collection.find_one(document_to_find)
    return json.loads(json_util.dumps(result))

def add_date_to_db(new_date_entry):
    db = client["dates-in-sg"]
    dates_collection = db.dates

    # TODO: Better schema validation
    if "location" in new_date_entry and "activity" in new_date_entry:
        result = dates_collection.insert_one(new_date_entry)
        return f"_id of inserted document: {result.inserted_id}"
    return None

def update_date_in_db(oid, updates):
    db = client["dates-in-sg"]
    dates_collection = db.dates
    reminder_to_update = {"_id": ObjectId(oid)}
    result = dates_collection.update_one(reminder_to_update, {"$set": updates})

    return f"Documents updated: {str(result.modified_count)}"

def delete_date_in_db(oid):
    db = client["dates-in-sg"]
    dates_collection = db.dates
    document_to_delete = {"_id": ObjectId(oid)}

    result = dates_collection.delete_one(document_to_delete)
    return f"Documents deleted: {str(result.deleted_count)}"

def add_review_to_db(oid, date_review):
    db = client["dates-in-sg"]
    dates_collection = db.dates

    find_duplicate = dates_collection.find_one({"_id": ObjectId(oid), "reviews.user_id": date_review['user_id']})
    if find_duplicate:
        return "Already Reviewed by User", 400

    date_review["date_added"] = datetime.datetime.now()
    date_to_review = {"_id": ObjectId(oid),}
    result = dates_collection.update_one(date_to_review,
                                         {"$push": {"reviews": date_review}})
    update_date_rating(oid)

    return f"Reviews added: {str(result.modified_count)}"

def update_review_in_db(oid, user_id, date_review):
    db = client["dates-in-sg"]
    dates_collection = db.dates
    date_review = dict(date_review)
    # date_review["date_added"] = datetime.datetime.now()
    date_to_review = {"_id": ObjectId(oid), "reviews.user_id": user_id}
    result = dates_collection.update_one(date_to_review,
                                         {"$set": {"reviews.$": date_review}})
    update_date_rating(oid)
    return f"Reviews modified: {str(result.modified_count)}"

def delete_review_in_db(oid, user_id):
    db = client["dates-in-sg"]
    dates_collection = db.dates
    review_to_delete = {"$pull": {"reviews": {"user_id": user_id}}}

    result = dates_collection.update_one({"_id": ObjectId(oid)}, review_to_delete)
    update_date_rating(oid)

    return f"Reviews deleted: {str(result.modified_count)}"

def update_date_rating(oid: str):
    """
    Given an oid returns the averages of the ratings in all reviews.
    """
    db = client["dates-in-sg"]
    dates_collection = db.dates
    select_by_oid = {"$match": {"_id": ObjectId(oid)}}
    get_average = {"$project": {"avg_rating": {"$avg": "$reviews.rating"}, "_id": 0}}
    pipeline = [select_by_oid, get_average]
    cursor = dates_collection.aggregate(pipeline)

    try:
        res = next(cursor)["avg_rating"]
        if type(res) == float:
            dates_collection.update_one({"_id": ObjectId(oid)}, {"$set": {"review_rating": round(res, 1)}})

    except:
        dates_collection.update_one({"_id": ObjectId(oid)}, {"$set": {"review_rating": float(0)}})
