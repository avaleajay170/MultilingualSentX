import io
import html
from datetime import datetime
from pathlib import Path

import emoji
import pandas as pd
import requests
from flask import Blueprint, request, jsonify, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from app.models.comments import create_comment
from app.models.analysis_results import save_result, get_results_by_batch
from app.models.batches import create_batch, update_batch_status, get_batch
from app.routes.analyze import run_pipeline
from app.db.connection import get_db

bulk_bp = Blueprint("bulk", __name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FONTS_DIR = PROJECT_ROOT / "fonts"
EMOJI_CACHE_DIR = FONTS_DIR / "emoji_cache"
DEVANAGARI_FONT_PATH = FONTS_DIR / "NotoSansDevanagari-Regular.ttf"
TWEMOJI_BASE_URL = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/72x72"

# Register the Devanagari font. Ensure the TTF file is in the expected path.
if not DEVANAGARI_FONT_PATH.is_file():
    raise FileNotFoundError(
        f"Noto Sans Devanagari font not found: {DEVANAGARI_FONT_PATH}"
    )
if "NotoDevanagari" not in pdfmetrics.getRegisteredFontNames():
    pdfmetrics.registerFont(TTFont("NotoDevanagari", str(DEVANAGARI_FONT_PATH)))

EMOJI_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _get_emoji_png(char):
    """Download and cache a colored Twemoji PNG; return None if unavailable."""
    codepoint = "-".join(f"{ord(ch):x}" for ch in char if ord(ch) != 0xFE0F)
    if not codepoint:
        return None
    image_path = EMOJI_CACHE_DIR / f"{codepoint}.png"
    if image_path.is_file():
        return image_path
    try:
        response = requests.get(f"{TWEMOJI_BASE_URL}/{codepoint}.png", timeout=5)
        response.raise_for_status()
        image_path.write_bytes(response.content)
        return image_path
    except (requests.RequestException, OSError):
        return None


def _comment_to_markup(text):
    """Escape text and render emoji as small colored inline PNG images."""
    parts = []
    cursor = 0
    for match in emoji.emoji_list(text):
        start, end = match["match_start"], match["match_end"]
        char = match["emoji"]
        parts.append(html.escape(text[cursor:start]))
        image_path = _get_emoji_png(char)
        if image_path:
            parts.append(
                f'<img src="{html.escape(str(image_path), quote=True)}" '
                'width="9" height="9" valign="middle"/>'
            )
        else:
            parts.append(html.escape(char))
        cursor = end
    parts.append(html.escape(text[cursor:]))
    return "".join(parts).replace("\n", "<br/>")


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
    processed = errors = 0
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
                model_used=analysis["model_used"],
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
        "errors": errors,
    }), 201


@bulk_bp.route("/analyze/bulk/<batch_id>", methods=["GET"])
def get_bulk_results(batch_id):
    batch = get_batch(batch_id)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404
    results = get_results_by_batch(batch_id)
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for result in results:
        sentiment_counts[result["sentiment"]] = sentiment_counts.get(result["sentiment"], 0) + 1
    return jsonify({
        "batch_id": str(batch["_id"]),
        "filename": batch["filename"],
        "status": batch["status"],
        "total_comments": batch["total_comments"],
        "sentiment_breakdown": sentiment_counts,
        "results": [{
            "sentiment": result["sentiment"],
            "sentiment_confidence": result["sentiment_confidence"],
            "aspect": result["aspect"],
            "aspect_confidence": result.get("aspect_confidence"),
        } for result in results],
    }), 200


@bulk_bp.route("/analyze/bulk/<batch_id>/report", methods=["GET"])
def download_bulk_report(batch_id):
    batch = get_batch(batch_id)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404

    results = get_results_by_batch(batch_id)
    db = get_db()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    elements = []

    normal_style = ParagraphStyle(
        "UnicodeNormal", parent=styles["Normal"],
        fontName="NotoDevanagari", fontSize=9, leading=12,
    )
    title_style = ParagraphStyle(
        "UnicodeTitle", parent=styles["Title"],
        fontName="NotoDevanagari", fontSize=20, leading=24, spaceAfter=6,
    )
    heading_style = ParagraphStyle(
        "UnicodeHeading", parent=styles["Heading2"], fontName="NotoDevanagari",
    )
    cell_style = ParagraphStyle(
        "CommentCell", parent=normal_style, fontSize=8, leading=11, wordWrap="CJK",
    )

    elements.append(Paragraph("MultilingualSentX — Sentiment Analysis Report", title_style))
    elements.append(Paragraph(f"File: {html.escape(str(batch['filename']))}", normal_style))
    elements.append(Paragraph(
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", normal_style
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Summary", heading_style))
    summary_data = [["Total Comments", str(batch["total_comments"])], ["Status", str(batch["status"])]]
    summary_table = Table(summary_data, colWidths=[150, 300])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.extend([summary_table, Spacer(1, 16)])

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for result in results:
        sentiment_counts[result["sentiment"]] = sentiment_counts.get(result["sentiment"], 0) + 1
    elements.append(Paragraph("Sentiment Breakdown", heading_style))
    total = len(results) or 1
    sentiment_data = [["Sentiment", "Count", "Percentage"]]
    for label, count in sentiment_counts.items():
        sentiment_data.append([label, str(count), f"{count / total * 100:.1f}%"])
    sentiment_table = Table(sentiment_data, colWidths=[150, 100, 100])
    sentiment_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.extend([sentiment_table, Spacer(1, 16)])

    aspect_counts = {}
    for result in results:
        aspect_counts[result["aspect"]] = aspect_counts.get(result["aspect"], 0) + 1
    elements.append(Paragraph("Aspect Breakdown", heading_style))
    aspect_data = [["Aspect", "Count"]]
    for aspect, count in sorted(aspect_counts.items(), key=lambda item: -item[1]):
        aspect_data.append([str(aspect), str(count)])
    aspect_table = Table(aspect_data, colWidths=[200, 100])
    aspect_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.extend([aspect_table, Spacer(1, 16)])

    elements.append(Paragraph("Comment-Level Results", heading_style))
    detail_data = [[
        Paragraph("#", normal_style), Paragraph("Comment", normal_style),
        Paragraph("Sentiment", normal_style), Paragraph("Confidence", normal_style),
        Paragraph("Aspect", normal_style),
    ]]
    for i, result in enumerate(results, start=1):
        comment = db.comments.find_one({"_id": result["comment_id"]})
        comment_text = comment.get("text", "") if comment else ""
        detail_data.append([
            str(i),
            Paragraph(_comment_to_markup(str(comment_text)), cell_style),
            str(result["sentiment"]),
            f"{float(result['sentiment_confidence']) * 100:.1f}%",
            str(result["aspect"]),
        ])

    detail_table = Table(detail_data, colWidths=[25, 220, 70, 60, 80], repeatRows=1)
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "NotoDevanagari"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(detail_table)

    doc.build(elements)
    buffer.seek(0)
    return send_file(
        buffer, mimetype="application/pdf", as_attachment=True,
        download_name=f"sentiment_report_{batch_id}.pdf",
    )
