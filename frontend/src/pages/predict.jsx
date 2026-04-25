import { useState } from "react";
import { predictMatch } from "../api";

const TEAMS = [
  "Arsenal FC", "Aston Villa FC", "Bournemouth FC", "Brentford FC",
  "Brighton & Hove Albion FC", "Burnley FC", "Chelsea FC", "Crystal Palace FC",
  "Everton FC", "Fulham FC", "Liverpool FC", "Luton Town FC",
  "Manchester City FC", "Manchester United FC", "Newcastle United FC",
  "Nottingham Forest FC", "Sheffield United FC", "Tottenham Hotspur FC",
  "West Ham United FC", "Wolverhampton Wanderers FC"
];
export default function Predict() {
  const [home, setHome]     = useState(TEAMS[0]);
  const [away, setAway]     = useState(TEAMS[1]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = () => {
    if (home === away) return alert("Pick different teams");
    setLoading(true);
    predictMatch(home, away).then(res => {
      setResult(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  return (
    <div style={{ padding: "24px", maxWidth: "600px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "24px" }}>Match predictor</h1>

      <div style={{ display: "flex", gap: "16px", alignItems: "center", marginBottom: "20px" }}>
        <div style={{ flex: 1 }}>
          <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", color: "#888" }}>Home team</label>
          <select value={home} onChange={e => setHome(e.target.value)} style={{ width: "100%" }}>
            {TEAMS.map(t => <option key={t}>{t}</option>)}
          </select>
        </div>
        <span style={{ paddingTop: "24px", color: "#888", fontWeight: 500 }}>vs</span>
        <div style={{ flex: 1 }}>
          <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", color: "#888" }}>Away team</label>
          <select value={away} onChange={e => setAway(e.target.value)} style={{ width: "100%" }}>
            {TEAMS.map(t => <option key={t}>{t}</option>)}
          </select>
        </div>
      </div>

      <button onClick={handlePredict} disabled={loading}
        style={{ width: "100%", padding: "12px", background: "#378ADD",
                 color: "white", border: "none", borderRadius: "8px",
                 fontSize: "15px", cursor: "pointer" }}>
        {loading ? "Predicting..." : "Predict outcome"}
      </button>

      {result && (
        <div style={{ marginTop: "32px" }}>
          <h2 style={{ marginBottom: "16px", fontSize: "16px" }}>
            {result.home} vs {result.away}
          </h2>
          {[
            ["Home win", result.probabilities.home_win, "#378ADD"],
            ["Draw",     result.probabilities.draw,     "#888"],
            ["Away win", result.probabilities.away_win, "#E24B4A"],
          ].map(([label, pct, color]) => (
            <div key={label} style={{ marginBottom: "12px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px", fontSize: "13px" }}>
                <span>{label}</span>
                <span style={{ fontWeight: 500 }}>{pct}%</span>
              </div>
              <div style={{ background: "#f0f0f0", borderRadius: "4px", height: "8px" }}>
                <div style={{ background: color, height: "8px", borderRadius: "4px", width: `${pct}%`, transition: "width .5s" }} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
