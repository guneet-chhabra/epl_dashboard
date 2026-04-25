import requests, json, pandas as pd, time, os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Understat's internal team ID mapping
TEAM_IDS = {
    "Manchester City": 167, "Arsenal": 228, "Liverpool": 210,
    "Aston Villa": 229, "Tottenham": 211, "Chelsea": 212,
    "Newcastle United": 213, "Manchester United": 214,
    "West Ham": 215, "Brighton": 233, "Wolverhampton": 216,
    "Fulham": 217, "Bournemouth": 219, "Crystal Palace": 220,
    "Brentford": 189, "Nottingham Forest": 221, "Everton": 218,
    "Luton": 402, "Burnley": 222, "Sheffield United": 100,
}

def get_team_xg(team_name, team_id, season=2023):
    # This is Understat's actual internal API endpoint
    url = "https://understat.com/main/getTeamMatchesStats"
    payload = {
        "teamId": team_id,
        "season": season,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://understat.com/team/{team_name.replace(' ', '_')}/{season}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    resp = requests.post(url, data=payload, headers=headers)
    print(f"  {team_name}: status {resp.status_code}, size {len(resp.text)} chars")

    if resp.status_code != 200:
        print(f"  Failed: {resp.text[:200]}")
        return None

    try:
        data = resp.json()
    except Exception as e:
        print(f"  JSON error: {e} — response: {resp.text[:200]}")
        return None

    if not data.get("success"):
        print(f"  API returned success=false: {data}")
        return None

    rows = []
    for game in data.get("data", []):
        rows.append({
            "date":          game.get("date", "")[:10],
            "team":          team_name,
            "xg_for":        float(game.get("xG", 0)),
            "xg_against":    float(game.get("xGA", 0) if "xGA" in game else game.get("xGa", 0)),
            "goals_for":     int(game.get("scored", 0)),
            "goals_against": int(game.get("missed", 0)),
            "result":        game.get("result", ""),
            "home":          game.get("h_a", ""),
        })

    print(f"  Got {len(rows)} matches")
    return pd.DataFrame(rows) if rows else None

def generate_xg_from_matches():
    """
    Fallback: if Understat blocks us entirely, estimate xG from
    actual goals scored. Not as accurate but keeps the project working.
    """
    import numpy as np
    matches = pd.read_csv(BASE_DIR / "data/matches_2023.csv")
    matches = matches.dropna(subset=["home_goals", "away_goals"])

    rows = []
    for _, m in matches.iterrows():
        hg, ag = int(m["home_goals"]), int(m["away_goals"])
        # Add small noise to make xG slightly different from goals
        h_xg = round(max(0.1, hg + np.random.normal(0, 0.4)), 2)
        a_xg = round(max(0.1, ag + np.random.normal(0, 0.4)), 2)
        result_h = "W" if hg > ag else ("D" if hg == ag else "L")
        result_a = "L" if hg > ag else ("D" if hg == ag else "W")
        rows.append({"date": m["date"], "team": m["home_team"],
                     "xg_for": h_xg, "xg_against": a_xg,
                     "goals_for": hg, "goals_against": ag,
                     "result": result_h, "home": "h"})
        rows.append({"date": m["date"], "team": m["away_team"],
                     "xg_for": a_xg, "xg_against": h_xg,
                     "goals_for": ag, "goals_against": hg,
                     "result": result_a, "home": "a"})

    df = pd.DataFrame(rows)
    df.to_csv(BASE_DIR / "data/xg_per_match.csv", index=False)
    print(f"Generated {len(df)} synthetic xG rows from match results")
    print("Note: these are estimates — real xG from Understat is more accurate")

if __name__ == "__main__":
    os.makedirs(BASE_DIR / "data", exist_ok=True)
    dfs = []

    for team_name, team_id in TEAM_IDS.items():
        print(f"Fetching {team_name}...")
        df = get_team_xg(team_name, team_id, season=2023)
        if df is not None:
            dfs.append(df)
        time.sleep(1.5)

    if not dfs:
        print("\nAll failed — Understat may have changed their API again.")
        print("Falling back to generating synthetic xG data from match results...")
        generate_xg_from_matches()
    else:
        combined = pd.concat(dfs, ignore_index=True)
        combined.to_csv(BASE_DIR / "data/xg_per_match.csv", index=False)
        print(f"\nSaved {len(combined)} rows to data/xg_per_match.csv")


