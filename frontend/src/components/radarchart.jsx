import { useEffect, useRef } from "react";
import * as d3 from "d3";

const STATS = [
  { key: "goals",       label: "Goals",        max: 30 },
  { key: "assists",     label: "Assists",       max: 20 },
  { key: "xg",         label: "xG",            max: 25 },
  { key: "xag",        label: "xAG",           max: 15 },
  { key: "key_passes", label: "Key passes",    max: 100 },
  { key: "prog_carries",label: "Prog. carries", max: 200 },
];

export default function RadarChart({ player1, player2 }) {
  const svgRef = useRef();

  useEffect(() => {
    if (!player1 || !player2) return;
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();  // clear on re-render

    const W = 400, H = 400, cx = W / 2, cy = H / 2, R = 150;
    const N = STATS.length;
    const angleStep = (2 * Math.PI) / N;

    // Helper: get (x,y) for a given stat index and value 0-1
    const point = (i, val) => {
      const angle = i * angleStep - Math.PI / 2;
      return [cx + R * val * Math.cos(angle), cy + R * val * Math.sin(angle)];
    };

    // Draw concentric rings (0.25, 0.5, 0.75, 1.0)
    [0.25, 0.5, 0.75, 1.0].forEach(r => {
      const pts = STATS.map((_, i) => point(i, r)).map(p => p.join(",")).join(" ");
      svg.append("polygon").attr("points", pts)
        .attr("fill", "none").attr("stroke", "#e0e0e0").attr("stroke-width", 0.5);
    });

    // Draw axes
    STATS.forEach((_, i) => {
      const [x, y] = point(i, 1);
      svg.append("line")
        .attr("x1", cx).attr("y1", cy).attr("x2", x).attr("y2", y)
        .attr("stroke", "#e0e0e0").attr("stroke-width", 0.5);
    });

    // Draw axis labels
    STATS.forEach((stat, i) => {
      const [x, y] = point(i, 1.2);
      svg.append("text").text(stat.label)
        .attr("x", x).attr("y", y)
        .attr("text-anchor", "middle").attr("dominant-baseline", "central")
        .attr("font-size", "12px").attr("fill", "#666");
    });

    // Helper: draw player polygon
    const drawPlayer = (player, color, opacity) => {
      const pts = STATS.map((stat, i) => {
        const val = Math.min((player[stat.key] || 0) / stat.max, 1);
        return point(i, val);
      });
      const pointStr = pts.map(p => p.join(",")).join(" ");
      svg.append("polygon").attr("points", pointStr)
        .attr("fill", color).attr("fill-opacity", opacity)
        .attr("stroke", color).attr("stroke-width", 2);
    };

    drawPlayer(player1, "#378ADD", 0.2);
    drawPlayer(player2, "#E24B4A", 0.2);

    // Legend
    [[player1.name, "#378ADD"], [player2.name, "#E24B4A"]].forEach(([name, color], i) => {
      svg.append("rect").attr("x", 10).attr("y", 10 + i * 20)
        .attr("width", 12).attr("height", 12).attr("fill", color);
      svg.append("text").text(name)
        .attr("x", 28).attr("y", 21 + i * 20)
        .attr("font-size", "12px").attr("fill", "#333");
    });

  }, [player1, player2]);

  return <svg ref={svgRef} width={400} height={400} />;
}