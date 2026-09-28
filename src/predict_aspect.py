import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "saved_models/muril_aspect"

_tokenizer = None
_model = None

def _load():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        _model.eval()

def predict_aspect(text):
    _load()
    inputs = _tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = _model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]
        pred_id = int(torch.argmax(probs))
        confidence = float(probs[pred_id])

    label = _model.config.id2label[pred_id]
    return {
        "aspect": label.capitalize(),
        "confidence": round(confidence, 4)
    }