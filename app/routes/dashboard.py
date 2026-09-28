from flask import Blueprint, jsonify
from app.db.connection import get_db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/stats", methods=["GET"])
def dashboard_stats():
    db = get_db()

    total_comments = db.analysis_results.count_documents({})

    # Overall sentiment breakdown
    sentiment_pipeline = [
        {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
    ]
    sentiment_counts = {doc["_id"]: doc["count"] for doc in db.analysis_results.aggregate(sentiment_pipeline)}

    # Aspect-wise breakdown (aspect x sentiment)
    aspect_pipeline = [
        {"$group": {
            "_id": {"aspect": "$aspect", "sentiment": "$sentiment"},
            "count": {"$sum": 1}
        }}
    ]
    aspect_raw = db.analysis_results.aggregate(aspect_pipeline)

    aspect_breakdown = {}
    for row in aspect_raw:
        aspect = row["_id"]["aspect"]
        sentiment = row["_id"]["sentiment"]
        count = row["count"]
        aspect_breakdown.setdefault(aspect, {"Positive": 0, "Negative": 0, "Neutral": 0})
        aspect_breakdown[aspect][sentiment] = count

    return jsonify({
        "total_comments": total_comments,
        "overall": {
            "Positive": sentiment_counts.get("Positive", 0),
            "Negative": sentiment_counts.get("Negative", 0),
            "Neutral": sentiment_counts.get("Neutral", 0)
        },
        "aspect_analysis": aspect_breakdown
    }), 200

@dashboard_bp.route("/dashboard/recent", methods=["GET"])
def recent_analyses():
    db = get_db()
    results = list(
        db.analysis_results.find().sort("created_at", -1).limit(10)
    )

    output = []
    for r in results:
        comment = db.comments.find_one({"_id": r["comment_id"]})
        output.append({
            "text": comment["text"] if comment else "",
            "sentiment": r["sentiment"],
            "sentiment_confidence": r["sentiment_confidence"],
            "aspect": r["aspect"],
            "created_at": r["created_at"].isoformat()
        })

    return jsonify(output), 200