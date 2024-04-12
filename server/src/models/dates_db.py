import os
import json
import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util, ObjectId

def get_all_dates_from_db(collection):
    cursor = collection.find()
    result = []
    for document in cursor:
        document_cleaned = json.loads(json_util.dumps(document))
        result.append(document_cleaned)
    return result

def get_one_date_from_db(oid, collection):
    document_to_find = {"_id": ObjectId(oid)}
    result = collection.find_one(document_to_find)
    return json.loads(json_util.dumps(result))

def add_date_to_db(new_date_entry, collection):
    # TODO: Better schema validation
    if "location" in new_date_entry and "activity" in new_date_entry:
        result = collection.insert_one(new_date_entry)
        return f"_id of inserted document: {result.inserted_id}"
    return None

def update_date_in_db(oid, updates, collection):
    collection
    reminder_to_update = {"_id": ObjectId(oid)}
    result = collection.update_one(reminder_to_update, {"$set": updates})

    return f"Documents updated: {str(result.modified_count)}"

def delete_date_in_db(oid, collection):
    document_to_delete = {"_id": ObjectId(oid)}

    result = collection.delete_one(document_to_delete)
    return f"Documents deleted: {str(result.deleted_count)}"

def add_review_to_db(oid, date_review, collection):
    find_duplicate = collection.find_one({"_id": ObjectId(oid), "reviews.user_id": date_review['user_id']})
    if find_duplicate:
        return "Already Reviewed by User", 400

    date_review["date_added"] = datetime.datetime.now()
    date_to_review = {"_id": ObjectId(oid)}
    result = collection.update_one(date_to_review,
                                         {"$push": {"reviews": date_review}})
    
    update_date_rating(oid, collection)

    return f"Reviews added: {str(result.modified_count)}"

def update_review_in_db(oid, user_id, date_review, collection):
    date_review = dict(date_review)
    # date_review["date_added"] = datetime.datetime.now()
    date_to_review = {"_id": ObjectId(oid), "reviews.user_id": user_id}
    result = collection.update_one(date_to_review,
                                         {"$set": {"reviews.$": date_review}})
    update_date_rating(oid, collection)
    return f"Reviews modified: {str(result.modified_count)}"

def delete_review_in_db(oid, user_id, collection):
    review_to_delete = {"$pull": {"reviews": {"user_id": user_id}}}

    result = collection.update_one({"_id": ObjectId(oid)}, review_to_delete)
    update_date_rating(oid, collection)

    return f"Reviews deleted: {str(result.modified_count)}"

def update_date_rating(oid: str, collection):
    """
    Given an oid returns the averages of the ratings in all reviews.
    """
    select_by_oid = {"$match": {"_id": ObjectId(oid)}}
    get_average = {"$project": {"avg_rating": {"$avg": "$reviews.rating"}, "review_count": {"$size": "$reviews"}}}
    pipeline = [select_by_oid, get_average]

    cursor = collection.aggregate(pipeline)

    try:
        res = next(cursor)
        avg_rating = res["avg_rating"]
        num_reviews = res["review_count"]
        collection.update_one({"_id": ObjectId(oid)}, {"$set": {"review_rating": round(avg_rating, 2), "number_of_reviews": num_reviews}})

    except:
        # review was just deleted (i.e. no reviews left)
        collection.update_one({"_id": ObjectId(oid)}, {"$set": {"review_rating": float(0), "number_of_reviews": 0}})