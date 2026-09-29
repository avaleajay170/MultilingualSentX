from flask import Blueprint, request, jsonify
from app.models.comments import create_comment
from app.models.analysis_results import save_result
from src.predict_sentiment import predict_sentiment
from src.predict_aspect import predict_aspect

analyze_bp = Blueprint("analyze", __name__)

def run_pipeline(text, explain=False):
    print("PIPELINE STEP 1 - Starting sentiment prediction", flush=True)
    sentiment_result = predict_sentiment(text)
    print("PIPELINE STEP 2 - Sentiment completed:", sentiment_result, flush=True)

    print("PIPELINE STEP 3 - Starting aspect prediction", flush=True)
    aspect_result = predict_aspect(text)
    print("PIPELINE STEP 4 - Aspect completed:", aspect_result, flush=True)

    if explain:
        print("PIPELINE STEP 5 - Generating SHAP/LIME explanation...", flush=True)
        from src.explain_sentiment import generate_explanation
        explanation = generate_explanation(text)
        print("PIPELINE STEP 6 - Explanation completed:", explanation, flush=True)
    else:
        explanation = {
            "shap_words": [],
            "lime_words": [],
            "llm_rationale": "Explanation skipped for bulk processing."
        }

    return {
        "detected_languages": ["Hindi", "Marathi", "English"],
        "sentiment": sentiment_result["sentiment"],
        "sentiment_confidence": sentiment_result["confidence"],
        "aspect": aspect_result["aspect"],
        "aspect_confidence": aspect_result["confidence"],
        "explanation": explanation,
        "model_used": "MuRIL (fine-tuned)"
    }

@analyze_bp.route("/analyze/single", methods=["POST"])
def analyze_single():
    print("\n========== ANALYZE REQUEST START ==========")

    data = request.get_json(silent=True)
    print("STEP 1 - JSON received:", data)

    if not data or "text" not in data:
        print("STEP 1 FAILED")
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"].strip()
    print("STEP 2 - Text:", text)

    if not text:
        print("STEP 2 FAILED")
        return jsonify({"error": "'text' cannot be empty"}), 400

    print("STEP 3 - Creating comment...")
    comment_id = create_comment(text, source="single")
    print("STEP 3 SUCCESS - comment_id:", comment_id)

    print("STEP 4 - Running pipeline (with explanation)...")
    analysis = run_pipeline(text, explain=True)
    print("STEP 4 SUCCESS - analysis:", analysis)

    print("STEP 5 - Saving result...")
    result_id = save_result(
        comment_id=comment_id,
        detected_languages=analysis["detected_languages"],
        sentiment=analysis["sentiment"],
        sentiment_confidence=analysis["sentiment_confidence"],
        aspect=analysis["aspect"],
        aspect_confidence=analysis["aspect_confidence"],
        explanation=analysis["explanation"],
        model_used=analysis["model_used"]
    )
    print("STEP 5 SUCCESS - result_id:", result_id)

    print("STEP 6 - Returning response")

    return jsonify({
        "comment_id": comment_id,
        "result_id": result_id,
        **analysis
    }), 201