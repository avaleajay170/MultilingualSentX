import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getDashboardStats, getRecentAnalyses } from "../api";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [recent, setRecent] = useState([]);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    getDashboardStats()
      .then(setStats)
      .catch((err) => setError(err.message));

    getRecentAnalyses()
      .then(setRecent)
      .catch((err) => setError(err.message));
  }, []);

  const openAnalysis = (item) => {
    navigate("/results", {
      state: {
        inputText: item.text,
        result: item
      }
    });
  };

  return (
    <div className="dashboard">

      <h1>Dashboard</h1>

      <p className="dashboard-subtitle">
        Overview of multilingual sentiment analysis
      </p>

      {error && (
        <p style={{ color: "#dc2626" }}>
          {error}
        </p>
      )}


      {/* =========================
          STATISTICS
      ========================= */}

      <div className="stats-grid">

        <div className="stat-card">
          <h3>Total Analyses</h3>
          <p>
            {stats ? stats.total_comments : 0}
          </p>
        </div>

        <div className="stat-card">
          <h3>Positive</h3>
          <p>
            {stats ? stats.overall.Positive : 0}
          </p>
        </div>

        <div className="stat-card">
          <h3>Negative</h3>
          <p>
            {stats ? stats.overall.Negative : 0}
          </p>
        </div>

        <div className="stat-card">
          <h3>Neutral</h3>
          <p>
            {stats ? stats.overall.Neutral : 0}
          </p>
        </div>

      </div>


      {/* =========================
          ASPECT BREAKDOWN
      ========================= */}

      <div className="dashboard-section">

        <h2>Aspect-wise Breakdown</h2>

        {stats &&
        Object.keys(stats.aspect_analysis).length > 0 ? (

          <table>

            <thead>
              <tr>
                <th>Aspect</th>
                <th>Positive</th>
                <th>Negative</th>
                <th>Neutral</th>
              </tr>
            </thead>

            <tbody>

              {Object.entries(
                stats.aspect_analysis
              ).map(([aspect, counts]) => (

                <tr key={aspect}>

                  <td>{aspect}</td>

                  <td>{counts.Positive}</td>

                  <td>{counts.Negative}</td>

                  <td>{counts.Neutral}</td>

                </tr>

              ))}

            </tbody>

          </table>

        ) : (

          <p>
            No analysis has been performed yet.
          </p>

        )}

      </div>


      {/* =========================
          RECENT ANALYSIS
      ========================= */}

      <div className="dashboard-section">

        <div className="recent-header">

          <div>
            <h2>Recent Analysis</h2>

            <p>
              Click any analysis to view the complete result.
            </p>
          </div>

        </div>


        {recent.length > 0 ? (

          <table className="recent-analysis-table">

            <thead>

              <tr>
                <th>Comment</th>
                <th>Sentiment</th>
                <th>Confidence</th>
                <th>Aspect</th>
              </tr>

            </thead>

            <tbody>

              {recent.map((item, idx) => (

                <tr
                  key={item.result_id || idx}
                  className="analysis-row"
                  onClick={() => openAnalysis(item)}
                >

                  <td
                    className="comment-cell"
                    title="Click to view full analysis"
                  >
                    {item.text.length > 60
                      ? item.text.slice(0, 60) + "..."
                      : item.text}
                  </td>

                  <td>
                    {item.sentiment}
                  </td>

                  <td>
                    {(item.sentiment_confidence * 100).toFixed(1)}%
                  </td>

                  <td>
                    {item.aspect}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        ) : (

          <p>
            No analysis has been performed yet.
          </p>

        )}

      </div>

    </div>
  );
}

export default Dashboard;