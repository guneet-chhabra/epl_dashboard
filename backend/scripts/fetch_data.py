import requests, os, json, pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# This finds the .env file relative to THIS script's location
BASE_DIR = Path(__file__).resolve().parent.parent  # goes up from scripts/ to backend/
load_dotenv(BASE_DIR / ".env")

import os

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

def get_epl_matches(season=2023):
    # competition code for EPL is "PL"
    url = f"{BASE}/competitions/PL/matches?season={season}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()  # raises error if API call fails
    data = resp.json()
    matches = data["matches"]
    rows = []
    for m in matches:
        rows.append({
            "match_id":     m["id"],
            "matchday":     m["matchday"],
            "date":         m["utcDate"][:10],
            "status":       m["status"],
            "home_team":    m["homeTeam"]["name"],
            "away_team":    m["awayTeam"]["name"],
            "home_goals":   m["score"]["fullTime"]["home"],
            "away_goals":   m["score"]["fullTime"]["away"],
        })
    df = pd.DataFrame(rows)
    df.to_csv("data/matches_2023.csv", index=False)
    print(f"Saved {len(df)} matches")

def get_epl_standings(season=2023):
    url = f"{BASE}/competitions/PL/standings?season={season}"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    table = data["standings"][0]["table"]  # [0] = overall table
    rows = []
    for entry in table:
        rows.append({
            "position": entry["position"],
            "team":     entry["team"]["name"],
            "played":   entry["playedGames"],
            "won":      entry["won"],
            "drawn":    entry["draw"],
            "lost":     entry["lost"],
            "gf":       entry["goalsFor"],
            "ga":       entry["goalsAgainst"],
            "gd":       entry["goalDifference"],
            "points":   entry["points"],
        })
    df = pd.DataFrame(rows)
    df.to_csv("data/standings_2023.csv", index=False)
    print(f"Saved {len(df)} teams")

if __name__ == "__main__":
    get_epl_matches(2023)
    get_epl_standings(2023)
