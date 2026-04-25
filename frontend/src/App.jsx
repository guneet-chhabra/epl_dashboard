import { Routes, Route, Link } from "react-router-dom"
import Teams from "./pages/Teams"
import Predict from "./pages/Predict"
import Players from "./pages/Players"

export default function App() {
  return (
    <div style={{ fontFamily: "Inter, sans-serif", minHeight: "100vh", background: "#f9f9f9" }}>
      <nav style={{
        background: "#1a1a2e", padding: "14px 32px",
        display: "flex", alignItems: "center", gap: "32px"
      }}>
        <span style={{ color: "white", fontWeight: 700, fontSize: "18px" }}>⚽ EPL Dashboard</span>
        <Link to="/"        style={{ color: "#aaa", textDecoration: "none", fontSize: "14px" }}>Teams</Link>
        <Link to="/players" style={{ color: "#aaa", textDecoration: "none", fontSize: "14px" }}>Players</Link>
        <Link to="/predict" style={{ color: "#aaa", textDecoration: "none", fontSize: "14px" }}>Predict</Link>
      </nav>
      <Routes>
        <Route path="/"        element={<Teams />} />
        <Route path="/players" element={<Players />} />
        <Route path="/predict" element={<Predict />} />
      </Routes>
    </div>
  )
}