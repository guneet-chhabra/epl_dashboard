import { useState, useEffect } from "react"
import { getPlayers } from "../api"
import RadarChart from "../components/RadarChart"

export default function Players() {
  const [players, setPlayers]   = useState([])
  const [search, setSearch]     = useState("")
  const [player1, setPlayer1]   = useState(null)
  const [player2, setPlayer2]   = useState(null)

  useEffect(() => { getPlayers().then(res => setPlayers(res.data)) }, [])

  const filtered = players.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase())
  ).slice(0, 50)

  const selectPlayer = (p) => {
    if (!player1)      setPlayer1(p)
    else if (!player2) setPlayer2(p)
    else { setPlayer1(p); setPlayer2(null) }
  }

  return (
    <div style={{ padding: "32px", maxWidth: "1100px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "8px" }}>Players</h1>
      <p style={{ color: "#888", marginBottom: "20px", fontSize: "14px" }}>
        Select two players to compare on the radar chart
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "32px" }}>
        <div>
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Search player..."
            style={{ width: "100%", padding: "10px 14px", borderRadius: "8px",
                     border: "1px solid #ddd", marginBottom: "12px", fontSize: "14px" }} />

          <div style={{ background: "white", borderRadius: "12px", overflow: "hidden",
                        boxShadow: "0 1px 4px #0001", maxHeight: "500px", overflowY: "auto" }}>
            {filtered.map(p => (
              <div key={p.id} onClick={() => selectPlayer(p)}
                style={{ padding: "10px 16px", cursor: "pointer", fontSize: "13px",
                         borderBottom: "1px solid #f5f5f5",
                         background: (player1?.id === p.id || player2?.id === p.id) ? "#f0f7ff" : "white",
                         display: "flex", justifyContent: "space-between" }}>
                <span style={{ fontWeight: 500 }}>{p.name}</span>
                <span style={{ color: "#888" }}>{p.team}</span>
              </div>
            ))}
          </div>

          <div style={{ marginTop: "12px", fontSize: "13px", color: "#888" }}>
            {player1 && <div>🔵 {player1.name}</div>}
            {player2 && <div>🔴 {player2.name}</div>}
            {!player1 && <div>Click a player to select</div>}
            {player1 && !player2 && <div>Click another player to compare</div>}
          </div>
        </div>

        <div style={{ background: "white", borderRadius: "12px", padding: "24px",
                      boxShadow: "0 1px 4px #0001", display: "flex",
                      alignItems: "center", justifyContent: "center" }}>
          {player1 && player2
            ? <RadarChart player1={player1} player2={player2} />
            : <p style={{ color: "#ccc", fontSize: "14px" }}>Select two players to see radar chart</p>
          }
        </div>
      </div>
    </div>
  )
}