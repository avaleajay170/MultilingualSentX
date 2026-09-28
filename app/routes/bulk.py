import pandas as pd
from flask import Blueprint, request, jsonify
from app.models.comments import create_comment
from app.models.analysis_results import save_result
from app.models.batches import create_batch, update_batch_status
from app.routes.analyze import run_pipeline

bulk_bp = Blueprint("bulk", __name__)

@bulk_bp.route("/analyze/bulk", methods=["POST"])
def analyze_bulk():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Use form field name 'file'."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only .csv files are supported."}), 400

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Failed to parse CSV: {str(e)}"}), 400

    if "comment" not in df.columns:
        return jsonify({"error": "CSV must have a 'comment' column."}), 400

    df = df.dropna(subset=["comment"])
    total = len(df)
    if total == 0:
        return jsonify({"error": "No valid comments found in CSV."}), 400

    batch_id = create_batch(filename=file.filename, total_comments=total)

    processed = 0
    errors = 0

    for _, row in df.iterrows():
        text = str(row["comment"]).strip()
        if not text:
            errors += 1
            continue
        try:
            comment_id = create_comment(text, source="bulk", batch_id=batch_id)
            analysis = run_pipeline(text)
            save_result(
                comment_id=comment_id,
                detected_languages=analysis["detected_languages"],
                sentiment=analysis["sentiment"],
                sentiment_confidence=analysis["sentiment_confidence"],
                aspect=analysis["aspect"],
                aspect_confidence=analysis["aspect_confidence"],
                explanation=analysis["explanation"],
                model_used=analysis["model_used"]
            )
            processed += 1
        except Exception:
            errors += 1

    update_batch_status(batch_id, "completed" if errors == 0 else "completed_with_errors")

    return jsonify({
        "batch_id": batch_id,
        "filename": file.filename,
        "total_comments": total,
        "processed": processed,
        "errors": errors
    }), 201