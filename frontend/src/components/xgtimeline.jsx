import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from "recharts"

export default function XGTimeline({ data, team }) {
  const chartData = data.map((d, i) => ({
    match: i + 1,
    xG:    parseFloat(d.xg_for?.toFixed(2) ?? 0),
    xGA:   parseFloat(d.xg_against?.toFixed(2) ?? 0),
  }))

  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={chartData}>
        <XAxis dataKey="match" label={{ value: "Match", position: "insideBottom", offset: -2 }} />
        <YAxis />
        <Tooltip />
        <ReferenceLine y={1.5} stroke="#ddd" strokeDasharray="4 4" />
        <Line type="monotone" dataKey="xG"  stroke="#378ADD" dot={false} strokeWidth={2} name="xG for" />
        <Line type="monotone" dataKey="xGA" stroke="#E24B4A" dot={false} strokeWidth={2} name="xG against" />
      </LineChart>
    </ResponsiveContainer>
  )
}