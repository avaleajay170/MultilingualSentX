function Analysis() {
  return (
    <div className="analysis-page">

      {/* Page Header */}
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


      {/* Analysis Card */}
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


        {/* Text Input */}
        <textarea
          placeholder="Example: Aaj ka movie bahut amazing tha, but ending thodi disappointing thi..."
          rows="9"
        ></textarea>


        {/* Character Information */}
        <div className="input-footer">
          <span>
            Supports multilingual code-mixed text
          </span>

          <span>
            0 / 1000 characters
          </span>
        </div>


        {/* Buttons */}
        <div className="analysis-actions">

          <button className="analyze-button">
            Analyze Sentiment
          </button>

          <button className="secondary-button">
            Clear
          </button>

        </div>

      </div>


      {/* Information Cards */}
      <div className="analysis-info-grid">

        <div className="info-card">
          <div className="info-icon">🌐</div>

          <h3>Multilingual</h3>

          <p>
            Supports Hindi, Marathi and English
            code-mixed text.
          </p>
        </div>


        <div className="info-card">
          <div className="info-icon">🧠</div>

          <h3>AI Powered</h3>

          <p>
            Uses multilingual AI models to
            understand sentiment.
          </p>
        </div>


        <div className="info-card">
          <div className="info-icon">💡</div>

          <h3>Explainable</h3>

          <p>
            Provides understandable insights
            behind the prediction.
          </p>
        </div>

      </div>

    </div>
  )
}

export default Analysis