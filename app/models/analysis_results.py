from datetime import datetime
from bson import ObjectId
from app.db.connection import get_db

def save_result(comment_id, detected_languages, sentiment, sentiment_confidence,
                 aspect, explanation, model_used="MuRIL", aspect_confidence=None):
    db = get_db()
    result = {
        "comment_id": ObjectId(comment_id),
        "detected_languages": detected_languages,
        "sentiment": sentiment,
        "sentiment_confidence": sentiment_confidence,
        "aspect": aspect,
        "aspect_confidence": aspect_confidence,
        "explanation": explanation,
        "model_used": model_used,
        "created_at": datetime.utcnow()
    }
    inserted = db.analysis_results.insert_one(result)
    return str(inserted.inserted_id)

def get_result_by_comment(comment_id):
    db = get_db()
    return db.analysis_results.find_one({"comment_id": ObjectId(comment_id)})

def get_results_by_batch(batch_id):
    db = get_db()
    comment_ids = [c["_id"] for c in db.comments.find({"batch_id": ObjectId(batch_id)}, {"_id": 1})]
    return list(db.analysis_results.find({"comment_id": {"$in": comment_ids}}))