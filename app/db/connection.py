import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "multilingualsentx")

client = None
db = None

def init_db():
    """Initialize the MongoDB connection. Call this once at app startup."""
    global client, db
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client[DB_NAME]
    try:
        client.admin.command('ping')
        print("MongoDB connected successfully.")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise
    return db

def get_db():
    """Return the active db instance, initializing if needed."""
    global db
    if db is None:
        return init_db()
    return db