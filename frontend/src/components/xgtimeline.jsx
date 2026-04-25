import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip,
         Legend, ResponsiveContainer, ReferenceLine } from "recharts";
import { getTeamXG } from "../api";

const TEAMS = ["Arsenal", "Manchester City", "Liverpool",
               "Chelsea", "Tottenham", "Manchester United"];

export default function XGTimeline() {
  const [team1, setTeam1]   = useState("Arsenal");
  const [team2, setTeam2]   = useState("Manchester City");
  const [data1, setData1]   = useState([]);
  const [data2, setData2]   = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    Promise.all([getTeamXG(team1), getTeamXG(team2)]).then(([r1, r2]) => {
      setData1(r1.data.map((d, i) => ({ match: i + 1, xg: +d.xg_for.toFixed(2) })));
      setData2(r2.data.map((d, i) => ({ match: i + 1, xg: +d.xg_for.toFixed(2) })));
      setLoading(false);
    });
  }, [team1, team2]);

  // Merge both datasets by match number for Recharts
  const merged = data1.map((d, i) => ({
    match: d.match,
    [team1]: d.xg,
    [team2]: data2[i]?.xg ?? null,
  }));

  return (
    <div style={{ padding: "24px" }}>
      <div style={{ display: "flex", gap: "12px", marginBottom: "20px" }}>
        <select value={team1} onChange={e => setTeam1(e.target.value)}>
          {TEAMS.map(t => <option key={t}>{t}</option>)}
        </select>
        <span style={{ alignSelf: "center", color: "#888" }}>vs</span>
        <select value={team2} onChange={e => setTeam2(e.target.value)}>
          {TEAMS.map(t => <option key={t}>{t}</option>)}
        </select>
      </div>
      {loading ? <p>Loading...</p> : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={merged}>
            <XAxis dataKey="match" label={{ value: "Match", position: "bottom" }} />
            <YAxis label={{ value: "xG", angle: -90, position: "insideLeft" }} />
            <Tooltip />
            <Legend />
            <ReferenceLine y={1.5} stroke="#ccc" strokeDasharray="4 4" />
            <Line type="monotone" dataKey={team1} stroke="#378ADD" dot={false} strokeWidth={2} />
            <Line type="monotone" dataKey={team2} stroke="#E24B4A" dot={false} strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
