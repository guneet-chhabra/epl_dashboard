import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "players_2023.csv")

def load_and_clean_players():
    if not os.path.exists(file_path):
        print("❌ File not found")
        return

    # 🔥 robust read (handles messy CSV)
    df = pd.read_csv(file_path, sep=None, engine="python", on_bad_lines="skip")

    # 🔁 Normalize column names (handles FBref/Understat mix)
    df.columns = [col.strip().lower() for col in df.columns]

    rename_map = {
        "player": "player",
        "player_name": "player",

        "squad": "team",
        "team": "team",
        "team_title": "team",

        "pos": "position",
        "position": "position",

        "age": "age",

        "mp": "matches",
        "games": "matches",

        "gls": "goals",
        "goals": "goals",

        "ast": "assists",
        "assists": "assists",

        "xg": "xg",
        "xa": "xag",
        "xag": "xag"
    }

    df = df.rename(columns=rename_map)

    # 🧹 Remove junk rows
    if "player" in df.columns:
        df = df.dropna(subset=["player"])
        df = df[df["player"].str.lower() != "player"]

    # 🎯 Keep useful columns
    cols = ["player", "team", "position", "age", "matches", "goals", "assists", "xg", "xag"]
    cols = [c for c in cols if c in df.columns]
    df = df[cols]

    # 🔢 Convert numeric safely
    for col in cols:
        if col not in ["player", "team", "position"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 💾 overwrite clean file
    df.to_csv(file_path, index=False)

    print(f"✅ Loaded & cleaned {len(df)} players")
    print(df.head())


if __name__ == "__main__":
    load_and_clean_players()
