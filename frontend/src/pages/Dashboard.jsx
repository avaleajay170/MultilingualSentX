function Dashboard() {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <p className="dashboard-subtitle">
        Overview of multilingual sentiment analysis
      </p>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Analyses</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Positive</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Negative</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Neutral</h3>
          <p>0</p>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Recent Analysis</h2>

        <p>
          No analysis has been performed yet.
        </p>
      </div>
    </div>
  )
}

export default Dashboard