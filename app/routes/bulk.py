import pandas as pd
from flask import Blueprint, request, jsonify, send_file
from app.models.comments import create_comment
from app.models.analysis_results import save_result, get_results_by_batch
from app.models.batches import create_batch, update_batch_status, get_batch
from app.routes.analyze import run_pipeline
from app.db.connection import get_db

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


@bulk_bp.route("/analyze/bulk/<batch_id>", methods=["GET"])
def get_bulk_results(batch_id):
    batch = get_batch(batch_id)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404

    results = get_results_by_batch(batch_id)

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in results:
        sentiment_counts[r["sentiment"]] = sentiment_counts.get(r["sentiment"], 0) + 1

    return jsonify({
        "batch_id": str(batch["_id"]),
        "filename": batch["filename"],
        "status": batch["status"],
        "total_comments": batch["total_comments"],
        "sentiment_breakdown": sentiment_counts,
        "results": [
            {
                "sentiment": r["sentiment"],
                "sentiment_confidence": r["sentiment_confidence"],
                "aspect": r["aspect"],
                "aspect_confidence": r.get("aspect_confidence")
            } for r in results
        ]
    }), 200
    
    from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from datetime import datetime

@bulk_bp.route("/analyze/bulk/<batch_id>/report", methods=["GET"])
def download_bulk_report(batch_id):
    batch = get_batch(batch_id)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404

    results = get_results_by_batch(batch_id)
    db = get_db()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=20, spaceAfter=6)
    elements.append(Paragraph("MultilingualSentX — Sentiment Analysis Report", title_style))
    elements.append(Paragraph(f"File: {batch['filename']}", styles["Normal"]))
    elements.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Summary section
    elements.append(Paragraph("Summary", styles["Heading2"]))
    summary_data = [
        ["Total Comments", str(batch["total_comments"])],
        ["Status", batch["status"]],
    ]
    summary_table = Table(summary_data, colWidths=[150, 300])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 16))

    # Sentiment breakdown
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in results:
        sentiment_counts[r["sentiment"]] = sentiment_counts.get(r["sentiment"], 0) + 1

    elements.append(Paragraph("Sentiment Breakdown", styles["Heading2"]))
    sentiment_data = [["Sentiment", "Count", "Percentage"]]
    total = len(results) or 1
    for label, count in sentiment_counts.items():
        pct = f"{(count/total)*100:.1f}%"
        sentiment_data.append([label, str(count), pct])
    sentiment_table = Table(sentiment_data, colWidths=[150, 100, 100])
    sentiment_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(sentiment_table)
    elements.append(Spacer(1, 16))

    # Aspect breakdown
    aspect_counts = {}
    for r in results:
        aspect_counts.setdefault(r["aspect"], 0)
        aspect_counts[r["aspect"]] += 1

    elements.append(Paragraph("Aspect Breakdown", styles["Heading2"]))
    aspect_data = [["Aspect", "Count"]]
    for aspect, count in sorted(aspect_counts.items(), key=lambda x: -x[1]):
        aspect_data.append([aspect, str(count)])
    aspect_table = Table(aspect_data, colWidths=[200, 100])
    aspect_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(aspect_table)
    elements.append(Spacer(1, 16))

    # Per-comment detail table
    elements.append(Paragraph("Comment-Level Results", styles["Heading2"]))
    cell_style = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=8, leading=10)
    detail_data = [["#", "Comment", "Sentiment", "Confidence", "Aspect"]]

    for i, r in enumerate(results, start=1):
        comment = db.comments.find_one({"_id": r["comment_id"]})
        text = comment["text"] if comment else ""
        detail_data.append([
            str(i),
            Paragraph(text, cell_style),
            r["sentiment"],
            f"{r['sentiment_confidence']*100:.1f}%",
            r["aspect"]
        ])

    detail_table = Table(detail_data, colWidths=[25, 220, 70, 60, 80], repeatRows=1)
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(detail_table)

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"sentiment_report_{batch_id}.pdf"
    )