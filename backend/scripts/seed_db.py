
import pandas as pd, sys
sys.path.append(".")
from app.database import engine, SessionLocal
from app.models import Base, Match, Player, TeamXG
from sqlalchemy.orm import Session
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, "data", "matches_2023.csv")
file_path2 = os.path.join(BASE_DIR, "data", "players_2023.csv")

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created")

db: Session = SessionLocal()

# Load matches
df = pd.read_csv(file_path)
for _, row in df.iterrows():
    m = Match(
        id=row["match_id"], matchday=row["matchday"],
        date=row["date"], home_team=row["home_team"],
        away_team=row["away_team"],
        home_goals=None if pd.isna(row["home_goals"]) else int(row["home_goals"]),
        away_goals=None if pd.isna(row["away_goals"]) else int(row["away_goals"]),
        status=row["status"]
    )
    db.merge(m)  # merge = upsert (insert or update)

# ── Load players ──────────────────────────────────────────
print("Loading players...")
df = pd.read_csv(file_path2)
print("Columns found:", df.columns.tolist())

def safe_int(val, default=0):
    try: return int(float(val))
    except: return default

def safe_float(val, default=0.0):
    try: return float(val)
    except: return default

loaded = 0
# Clean up mid-season transfers — keep only the first team listed
df["team"] = df["team"].apply(lambda x: str(x).split(",")[0].strip())
for _, row in df.iterrows():
    name = str(row.get("player", row.get("Player", ""))).strip()
    if not name or name == "Player" or name == "nan":
        continue

    p = Player(
        name           = name,
        team           = str(row.get("team", row.get("Squad", ""))).strip(),
        position       = str(row.get("position", row.get("Pos", "FW"))),  # default FW if missing
        goals          = safe_int(row.get("goals",        row.get("Gls",  0))),
        assists        = safe_int(row.get("assists",       row.get("Ast",  0))),  # will be 0 if missing
        xg             = safe_float(row.get("xg",         row.get("xG",   0))),
        xag            = safe_float(row.get("xag",        row.get("xAG",  0))),
        key_passes     = safe_int(row.get("key_passes",   row.get("KP",   0))),
        prog_carries   = safe_int(row.get("prog_carries", row.get("PrgC", 0))),
        matches_played = safe_int(row.get("matches",      row.get("MP",   0))),
    )
    db.add(p)
    loaded += 1

db.commit()
print(f"Loaded {loaded} players")
db.commit()
db.close()
print("Database seeded!")