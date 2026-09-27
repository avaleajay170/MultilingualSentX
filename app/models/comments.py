from datetime import datetime
from bson import ObjectId
from app.db.connection import get_db

def create_comment(text, source="single", batch_id=None):
    db = get_db()
    comment = {
        "text": text,
        "source": source,
        "batch_id": ObjectId(batch_id) if batch_id else None,
        "created_at": datetime.utcnow()
    }
    result = db.comments.insert_one(comment)
    return str(result.inserted_id)

def get_comment(comment_id):
    db = get_db()
    return db.comments.find_one({"_id": ObjectId(comment_id)})

def get_comments_by_batch(batch_id):
    db = get_db()
    return list(db.comments.find({"batch_id": ObjectId(batch_id)}))