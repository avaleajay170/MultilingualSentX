from datetime import datetime
from bson import ObjectId
from app.db.connection import get_db

def create_batch(filename, total_comments):
    db = get_db()
    batch = {
        "filename": filename,
        "total_comments": total_comments,
        "status": "processing",
        "created_at": datetime.utcnow()
    }
    result = db.batches.insert_one(batch)
    return str(result.inserted_id)

def update_batch_status(batch_id, status):
    db = get_db()
    db.batches.update_one({"_id": ObjectId(batch_id)}, {"$set": {"status": status}})

def get_batch(batch_id):
    db = get_db()
    return db.batches.find_one({"_id": ObjectId(batch_id)})