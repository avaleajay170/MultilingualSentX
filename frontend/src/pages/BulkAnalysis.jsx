import { useState } from "react";
import { analyzeBulk, getBulkResults } from "../api";

function BulkAnalysis() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [summary, setSummary] = useState(null);
  const [batchResults, setBatchResults] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      setError("Please choose a CSV file.");
      return;
    }
    setLoading(true);
    setError(null);
    setSummary(null);
    setBatchResults(null);

    try {
      const result = await analyzeBulk(file);
      setSummary(result);

      const details = await getBulkResults(result.batch_id);
      setBatchResults(details);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analysis-page">

      <div className="analysis-header">
        <span className="analysis-badge">BULK CSV ANALYSIS</span>
        <h1>Analyze Multiple Comments</h1>
        <p>Upload a CSV file with a "comment" column to analyze many comments at once.</p>
      </div>

      <div className="analysis-card">
        <div className="card-header">
          <div>
            <h2>Upload CSV</h2>
            <p>File must have a column named "comment".</p>
          </div>
        </div>

        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginTop: "12px" }}
        />

        {error && <p style={{ color: "#dc2626", marginTop: "8px" }}>{error}</p>}

        <div className="analysis-actions">
          <button className="analyze-button" onClick={handleUpload} disabled={loading}>
            {loading ? "Processing..." : "Upload & Analyze"}
          </button>
        </div>
      </div>

      {summary && (
        <div className="result-main-card" style={{ marginTop: "20px" }}>
          <div className="result-title">
            <div>
              <h2>Batch Summary</h2>
              <p>{summary.filename}</p>
            </div>
            <span className="result-status">Complete</span>
          </div>

          <div className="result-grid">
            <div className="result-card">
              <span className="result-card-label">TOTAL</span>
              <h3>{summary.total_comments}</h3>
              <p>Comments in file</p>
            </div>
            <div className="result-card">
              <span className="result-card-label">PROCESSED</span>
              <h3>{summary.processed}</h3>
              <p>Successfully analyzed</p>
            </div>
            <div className="result-card">
              <span className="result-card-label">ERRORS</span>
              <h3>{summary.errors}</h3>
              <p>Failed rows</p>
            </div>
          </div>
        </div>
      )}

      {batchResults && (
        <div className="dashboard-section" style={{ marginTop: "20px" }}>
          <h2>Sentiment Breakdown</h2>
          <table>
            <thead>
              <tr>
                <th>Sentiment</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(batchResults.sentiment_breakdown).map(([sentiment, count]) => (
                <tr key={sentiment}>
                  <td>{sentiment}</td>
                  <td>{count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

    </div>
  )
}

export default BulkAnalysis