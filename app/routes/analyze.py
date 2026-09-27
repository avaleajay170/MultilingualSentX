from flask import Blueprint, request, jsonify
from app.models.comments import create_comment
from app.models.analysis_results import save_result

analyze_bp = Blueprint("analyze", __name__)

def run_pipeline(text):
    """
    PLACEHOLDER — replace with real model inference once
    MuRIL/XLM-R training and SHAP/LIME/LLM integration are ready.
    """
    return {
        "detected_languages": ["Hindi", "Marathi", "English"],
        "sentiment": "Negative",
        "sentiment_confidence": 0.91,
        "aspect": "Delivery",
        "explanation": {
            "shap_words": ["late", "zali"],
            "lime_words": ["delivery", "late"],
            "llm_rationale": "Placeholder rationale — LLM integration pending."
        },
        "model_used": "placeholder"
    }

@analyze_bp.route("/analyze/single", methods=["POST"])
def analyze_single():
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "'text' cannot be empty"}), 400

    comment_id = create_comment(text, source="single")
    analysis = run_pipeline(text)
    result_id = save_result(
        comment_id=comment_id,
        detected_languages=analysis["detected_languages"],
        sentiment=analysis["sentiment"],
        sentiment_confidence=analysis["sentiment_confidence"],
        aspect=analysis["aspect"],
        explanation=analysis["explanation"],
        model_used=analysis["model_used"]
    )

    return jsonify({
        "comment_id": comment_id,
        "result_id": result_id,
        **analysis
    }), 201