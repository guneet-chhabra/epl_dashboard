import { useState, useEffect } from "react";
import { getTeamForm } from "../api";
import FormStrip from "../components/FormStrip";
import XGTimeline from "../components/XGTimeline";

const TEAMS = ["Arsenal", "Manchester City", "Liverpool",
               "Chelsea", "Tottenham", "Manchester United",
               "Aston Villa", "Newcastle", "Brighton", "West Ham"];

export default function Teams() {
  const [forms, setForms] = useState({});

  useEffect(() => {
    TEAMS.forEach(team => {
      getTeamForm(team).then(res => {
        setForms(prev => ({ ...prev, [team]: res.data }));
      });
    });
  }, []);

  return (
    <div style={{ padding: "24px", maxWidth: "900px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "24px" }}>Teams</h1>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #eee", textAlign: "left" }}>
            <th style={{ padding: "8px" }}>Team</th>
            <th style={{ padding: "8px" }}>Form (last 5)</th>
          </tr>
        </thead>
        <tbody>
          {TEAMS.map(team => (
            <tr key={team} style={{ borderBottom: "1px solid #f5f5f5" }}>
              <td style={{ padding: "12px 8px", fontWeight: 500 }}>{team}</td>
              <td style={{ padding: "12px 8px" }}>
                {forms[team] ? <FormStrip results={forms[team]} /> : "Loading..."}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <hr style={{ margin: "32px 0", border: "none", borderTop: "1px solid #eee" }} />
      <h2 style={{ marginBottom: "16px" }}>xG comparison</h2>
      <XGTimeline />
    </div>
  );
}