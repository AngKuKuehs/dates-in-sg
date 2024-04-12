import json

from bson import ObjectId, json_util
from src.models.dates_db import (
    get_all_dates_from_db,
    get_one_date_from_db,
    add_date_to_db,
    update_date_in_db,
    delete_date_in_db,
    add_review_to_db,
    update_review_in_db,
    delete_review_in_db
)
from src.db import get_test_collection

mock_collection = get_test_collection()

entries = [
        {"_id": ObjectId("60e6368482066d71ee0c59cf"), "location": "Location 1", "activity": "Activity 1", "number_of_reviews": 0, "review_rating": 0, "reviews": []},
        {"_id": ObjectId("60e6368482066d71ee0c59d0"), "location": "Location 2", "activity": "Activity 2", "number_of_reviews": 0, "review_rating": 0, "reviews": []}
    ]

def test_get_all_dates_from_db():
    mock_collection.insert_many(entries)
    result = get_all_dates_from_db(mock_collection)
    assert len(result) == 2

def test_get_one_date_from_db():
    result = get_one_date_from_db("60e6368482066d71ee0c59cf", mock_collection)
    result = json.loads(json_util.dumps(result))
    assert result == {"_id": {"$oid": "60e6368482066d71ee0c59cf"}, "location": "Location 1", "activity": "Activity 1", "number_of_reviews": 0, "review_rating": 0, "reviews": []}

def test_add_date_to_db():
    add_date_to_db({"_id": ObjectId("60e6368482066d71ee0c59df"), "location": "Location 3", "activity": "Activity 3", "number_of_reviews": 0, "review_rating": 0, "reviews": []},
                   mock_collection)
    result = get_all_dates_from_db(mock_collection)
    assert len(result) == 3

def test_update_date_in_db():
    before = get_one_date_from_db("60e6368482066d71ee0c59df", mock_collection)

    update_date_in_db("60e6368482066d71ee0c59df",
                      {"location": "Location 3.5", "activity": "Activity 3.5", "number_of_reviews": 0, "review_rating": 0, "reviews": []},
                      mock_collection)
    
    after = get_one_date_from_db("60e6368482066d71ee0c59df", mock_collection)

    assert after["_id"] == before["_id"] and after["_id"] == {"$oid": "60e6368482066d71ee0c59df"}
    assert after != before


def test_delete_date_in_db():
    delete_date_in_db("60e6368482066d71ee0c59df", mock_collection)
    result = get_all_dates_from_db(mock_collection)
    assert len(result) == 2
    result = get_one_date_from_db("60e6368482066d71ee0c59df", mock_collection)
    assert result == None
    result = get_all_dates_from_db(mock_collection)
    assert len(result) == 2
    

review_1_1 = {
    "title": "Location 1 is great!",
    "user_id": "User 1",
    "description": "Great place to Activity 1!",
    "rating": 5
}

review_1_2 = {
    "title": "Location 1 is not great!",
    "user_id": "User 2",
    "description": "Not great place to Activity 1!",
    "rating": 0
}

def test_add_review_to_db():
    date_id = "60e6368482066d71ee0c59cf"

    add_review_to_db(date_id, review_1_1, mock_collection)
    result = get_one_date_from_db(date_id, mock_collection)
    assert len(result["reviews"]) == 1
    assert result["review_rating"] == 5
    print(result)

    add_review_to_db(date_id, review_1_2, mock_collection)
    result = get_one_date_from_db(date_id, mock_collection)
    print(result)
    assert len(result["reviews"]) == 2
    assert result["review_rating"] == 2.5
   
def test_update_review_in_db():
    date_id = "60e6368482066d71ee0c59cf"
    result = get_one_date_from_db(date_id, mock_collection)
    print(result)
    review_id = result["reviews"][1]["user_id"]
    updated_review = {
        "title": "Nice!",
        "user_id": "User 2",
        "description": "Fantastic place!",
        "rating": 4}
    update_review_in_db(date_id, review_id, updated_review, mock_collection)
    result = get_one_date_from_db(date_id, mock_collection)
    assert result["reviews"][1] == updated_review
    assert result["review_rating"] == 4.5

def test_delete_review_in_db():
    date_id = "60e6368482066d71ee0c59cf"
    result = get_one_date_from_db(date_id, mock_collection)
    review_id_1 = result["reviews"][0]["user_id"]
    review_id_2 = result["reviews"][1]["user_id"]

    delete_review_in_db(date_id, review_id_1, mock_collection)
    result = get_one_date_from_db(date_id, mock_collection)
    assert result["number_of_reviews"] == 1

    delete_review_in_db(date_id, review_id_2, mock_collection)
    result = get_one_date_from_db(date_id, mock_collection)
    assert result["number_of_reviews"] == 0

    assert result["reviews"] == []
    assert result["review_rating"] == 0

