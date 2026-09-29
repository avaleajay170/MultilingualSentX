import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeSingle } from "../api";

function Analysis() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    if (loading) return;

    if (!text.trim()) {
      setError("Please enter some text to analyze.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeSingle(text);
      navigate("/results", { state: { result, inputText: text } });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText("");
    setError(null);
  };

  return (
    <div className="analysis-page">

      <div className="analysis-header">
        <span className="analysis-badge">
          AI SENTIMENT ANALYSIS
        </span>

        <h1>Analyze Your Text</h1>

        <p>
          Analyze Hindi, Marathi and English code-mixed text
          using multilingual AI models.
        </p>
      </div>

      <div className="analysis-card">

        <div className="card-header">
          <div>
            <h2>Enter your text</h2>
            <p>
              Paste or type a comment to analyze its sentiment.
            </p>
          </div>

          <span className="language-badge">
            Hindi • Marathi • English
          </span>
        </div>

        <textarea
          placeholder="Example: Aaj ka movie bahut amazing tha, but ending thodi disappointing thi..."
          rows="9"
          value={text}
          maxLength={1000}
          onChange={(e) => setText(e.target.value)}
        ></textarea>

        <div className="input-footer">
          <span>
            Supports multilingual code-mixed text
          </span>

          <span>
            {text.length} / 1000 characters
          </span>
        </div>

        {error && (
          <p style={{ color: "#dc2626", marginTop: "8px" }}>
            {error}
          </p>
        )}

        <div className="analysis-actions">

          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Sentiment"}
          </button>

          <button
            className="secondary-button"
            onClick={handleClear}
            disabled={loading}
          >
            Clear
          </button>

        </div>

      </div>

      <div className="analysis-info-grid">

        <div className="info-card">
          <div className="info-icon">🌐</div>

          <h3>Multilingual</h3>

          <p>
            Supports Hindi, Marathi and English code-mixed text.
          </p>
        </div>

        <div className="info-card">
          <div className="info-icon">🧠</div>

          <h3>AI Powered</h3>

          <p>
            Uses multilingual AI models to understand sentiment.
          </p>
        </div>

        <div className="info-card">
          <div className="info-icon">💡</div>

          <h3>Explainable</h3>

          <p>
            Provides understandable insights behind the prediction.
          </p>
        </div>

      </div>

    </div>
  );
}

export default Analysis;