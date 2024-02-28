from routes import app
import models.datesDB as mdb

from flask import request

@app.route("/get-all", methods=["GET"])
def get_all_dates():
    """
    Gets all date entries.

    Returns
    -------
    dict
        Details of all date entries.
    """
    return mdb.get_all_dates_from_db()

@app.route("/get-one", methods=["GET"])
def get_one_date():
    """
    Gets a date entry.

    Query Parameter
    ----------
    oid: str
        date entry _id

    Returns
    -------
    dict
        Details of date entry.
    """
    oid = request.args.get("oid")
    return mdb.get_one_date_from_db(oid)


@app.route("/add-date", methods=["POST"])
def add_date():
    """
    Adds a date entry.

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
    
    new_date_entry = request.get_json()
    new_date_entry = dict(new_date_entry)
    date_entry_resp = mdb.add_date_to_db(new_date_entry)

    return date_entry_resp if date_entry_resp else "Does not conform to Schema", 400

@app.route("/update-date", methods=["PUT"])
def update_date():
    """
    Updates a date entry.

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

    oid = request.args.get("oid")
    updates = request.get_json()

    return mdb.update_date_in_db(oid, updates)

@app.route("/delete-date", methods=["DELETE"])
def remove_date():
    """
    Deletes a date entry.

    Query Parameters
    ----------
    oid: str
        id_ of date entry to delete.

    Returns
    -------
    str
        Number of documents deleted.
    """
    oid = request.args.get("oid") 
    return mdb.delete_date_in_db(oid)

@app.route("/add-review", methods=["PUT"])
def add_review():  
    """
    Adds a review to a specified date entry.

    Query Parameters
    ----------
    oid: str
        id_ of date entry to update.

    Request Body
    ----------
    application/json
        JSON object formatted according to the schema

    Returns
    -------
    str
        Number of documents updated.
    """
    oid = request.args.get("oid")
    date_review = request.get_json()
    date_review = dict(date_review)
    
    return mdb.add_review_to_db(oid, date_review)

#TODO: review score not updating properly
@app.route("/update-review", methods=["PUT"])
def update_review():
    """
    Adds a review to a specified date entry.

    Query Parameters
    ----------
    oid: str
        id_ of date entry to update.

    Request Body
    ----------
    application/json
        JSON object formatted according to the schema

    Returns
    -------
    str
        Number of documents updated.
    """
    oid = request.args.get("oid")
    user_id = request.args.get("uid")
    date_review = request.get_json()
    return mdb.update_review_in_db(oid, user_id, date_review)

@app.route("/delete-review", methods=["DELETE"])
def delete_review():
    """
    Deletes a review to a specified date entry.

    Query Parameters
    ----------
    oid: str
        id_ of date entry to update.
    uid: str
        id_ of the user whose review is to be deleted.

    Returns
    -------
    str
        Number of documents updated.
    """
    oid = request.args.get("oid")
    user_id = request.args.get("uid")
    return mdb.delete_review_in_db(oid, user_id)
