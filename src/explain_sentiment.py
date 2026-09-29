import numpy as np
import torch
from lime.lime_text import LimeTextExplainer
import shap

import src.predict_sentiment as sentiment_module

LABELS = ["Negative", "Neutral", "Positive"]

def predict_proba(texts):
    """Takes a list of raw texts, returns an (n_samples, 3) probability array."""
    sentiment_module._load()
    tokenizer = sentiment_module._tokenizer
    model = sentiment_module._model

    inputs = tokenizer(list(texts), return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1).numpy()
    return probs

_lime_explainer = LimeTextExplainer(class_names=LABELS, split_expression=r"\s+", bow=False)

_shap_masker = shap.maskers.Text(tokenizer=r"\s+")
_shap_explainer = shap.Explainer(predict_proba, _shap_masker, output_names=LABELS)

def explain_with_lime(text, num_features=6):
    pred_id = int(np.argmax(predict_proba([text])[0]))
    exp = _lime_explainer.explain_instance(
        text, predict_proba, num_features=num_features, num_samples=80, labels=[pred_id]
    )
    word_weights = exp.as_list(label=pred_id)
    top_words = [w for w, weight in word_weights if weight > 0]
    return top_words[:num_features]

def explain_with_shap(text, num_features=6):
    shap_values = _shap_explainer([text], silent=True, max_evals=100)
    pred_id = int(np.argmax(predict_proba([text])[0]))

    tokens = shap_values.data[0]
    values = shap_values.values[0][:, pred_id]

    word_scores = list(zip(tokens, values))
    word_scores.sort(key=lambda x: abs(x[1]), reverse=True)

    top_words = [w.strip() for w, v in word_scores if v > 0 and w.strip()]
    return top_words[:num_features]

def generate_explanation(text):
    try:
        lime_words = explain_with_lime(text)
    except Exception as e:
        lime_words = []
        print(f"LIME explanation failed: {e}")

    try:
        shap_words = explain_with_shap(text)
    except Exception as e:
        shap_words = []
        print(f"SHAP explanation failed: {e}")

    important_words = list(dict.fromkeys(shap_words + lime_words))[:5]
    if important_words:
        rationale = f"The model's prediction was most influenced by: {', '.join(important_words)}."
    else:
        rationale = "Explanation could not be generated for this input."

    return {
        "shap_words": shap_words,
        "lime_words": lime_words,
        "llm_rationale": rationale
    }