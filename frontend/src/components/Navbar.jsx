import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">MultilingualSentX</Link>
      </div>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/analysis">Analysis</Link>
        <Link to="/results">Results</Link>
      </div>
    </nav>
  )
}

export default Navbar