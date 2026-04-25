export default function FormStrip({ results }) {
  const colors = { W: "#22c55e", D: "#f59e0b", L: "#ef4444" };

  return (
    <div style={{ display: "flex", gap: "4px", alignItems: "center" }}>
      {results.slice(0, 5).map((r, i) => (
        <div key={i} title={`${r.home} ${r.score} ${r.away} (${r.date})`}
          style={{
            width: "28px", height: "28px", borderRadius: "50%",
            background: colors[r.result],
            display: "flex", alignItems: "center", justifyContent: "center",
            color: "white", fontSize: "12px", fontWeight: 500,
            cursor: "default"
          }}>
          {r.result}
        </div>
      ))}
    </div>
  );
}