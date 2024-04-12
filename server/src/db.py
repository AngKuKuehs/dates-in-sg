import os

from dotenv import load_dotenv
from pymongo import MongoClient
import mongomock

load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]
client = MongoClient(MONGODB_URI)
db = client["dates-in-sg"]
dates_collection = db.dates

test_collection = mongomock.MongoClient().db.collection

def get_collection():
    return dates_collection

def get_test_collection():
    return test_collection