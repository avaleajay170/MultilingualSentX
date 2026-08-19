import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_db():
    global _client
    if _client is None:
        uri = os.getenv("MONGO_URI")
        _client = MongoClient(uri)
    return _client["multilingualsentx"]