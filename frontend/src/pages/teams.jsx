import { useState, useEffect } from "react"
import { getTeams, getTeamForm, getTeamXG } from "../api"
import FormStrip from "../components/formstrip"
import XGTimeline from "../components/xgtimeline"


export default function Teams() {
  const [teams, setTeams]   = useState([])
  const [forms, setForms]   = useState({})
  const [selected, setSelected] = useState(null)
  const [xgData, setXgData] = useState([])

  useEffect(() => {
    getTeams().then(res => {
      setTeams(res.data)
      res.data.forEach(team => {
        getTeamForm(team).then(r => {
          setForms(prev => ({ ...prev, [team]: r.data }))
        }).catch(() => {})
      })
    })
  }, [])

  const handleTeamClick = (team) => {
    setSelected(team)
    getTeamXG(team).then(res => setXgData(res.data))
  }

  return (
    <div style={{ padding: "32px", maxWidth: "1000px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "8px" }}>Teams</h1>
      <p style={{ color: "#888", marginBottom: "24px", fontSize: "14px" }}>Click a team to see their xG timeline</p>

      <table style={{ width: "100%", borderCollapse: "collapse", background: "white",
                      borderRadius: "12px", overflow: "hidden", boxShadow: "0 1px 4px #0001" }}>
        <thead>
          <tr style={{ background: "#f0f0f0", textAlign: "left" }}>
            <th style={{ padding: "12px 16px", fontSize: "13px", color: "#555" }}>Team</th>
            <th style={{ padding: "12px 16px", fontSize: "13px", color: "#555" }}>Last 5</th>
          </tr>
        </thead>
        <tbody>
          {teams.map(team => (
            <tr key={team}
              onClick={() => handleTeamClick(team)}
              style={{ borderTop: "1px solid #f0f0f0", cursor: "pointer",
                       background: selected === team ? "#f0f7ff" : "white" }}>
              <td style={{ padding: "12px 16px", fontWeight: 500 }}>{team}</td>
              <td style={{ padding: "12px 16px" }}>
                {forms[team] ? <FormStrip results={forms[team]} /> : <span style={{ color: "#ccc" }}>Loading...</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selected && (
        <div style={{ marginTop: "32px", background: "white", borderRadius: "12px",
                      padding: "24px", boxShadow: "0 1px 4px #0001" }}>
          <h2 style={{ marginBottom: "16px", fontSize: "16px" }}>{selected} — xG Timeline</h2>
          <XGTimeline data={xgData} team={selected} />
        </div>
      )}
    </div>
  )
}