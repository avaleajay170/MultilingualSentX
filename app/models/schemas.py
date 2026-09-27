"""
MongoDB collection schemas for MultilingualSentX.
MongoDB is schema-less; this file documents the expected shape
of each collection for reference across the team.

comments:
    _id: ObjectId
    text: str
    source: "single" | "bulk"
    batch_id: ObjectId | None
    created_at: datetime

analysis_results:
    _id: ObjectId
    comment_id: ObjectId
    detected_languages: list[str]
    sentiment: str
    sentiment_confidence: float
    aspect: str
    explanation: {
        shap_words: list[str],
        lime_words: list[str],
        llm_rationale: str
    }
    model_used: str
    created_at: datetime

batches:
    _id: ObjectId
    filename: str
    total_comments: int
    status: "processing" | "completed" | "failed"
    created_at: datetime
"""