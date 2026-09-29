import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Analysis from './pages/Analysis'
import BulkAnalysis from './pages/BulkAnalysis'
import Results from './pages/Results'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/analysis"
          element={<Analysis />}
        />

        <Route
          path="/bulk"
          element={<BulkAnalysis />}
        />

        <Route
          path="/results"
          element={<Results />}
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App