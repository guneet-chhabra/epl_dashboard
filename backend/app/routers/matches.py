from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import pickle, numpy as np

router = APIRouter()

# Load model once at startup
with open("ml/model.pkl", "rb") as f:
    MODEL, LE = pickle.load(f)

@router.get("/")
def get_all_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).order_by(models.Match.date.desc()).limit(50).all()
    return matches

@router.get("/predict")
def predict_match(home: str, away: str, db: Session = Depends(get_db)):
    def get_team_features(team_name, is_home, db):
        from sqlalchemy import or_
        recent = db.query(models.Match).filter(
            or_(models.Match.home_team == team_name,
                models.Match.away_team == team_name),
            models.Match.status == "FINISHED"
        ).order_by(models.Match.date.desc()).limit(5).all()

        if len(recent) < 3:
            raise HTTPException(400, f"Not enough data for {team_name}")

        xg_records = db.query(models.TeamXG).filter(
            models.TeamXG.team == team_name
        ).order_by(models.TeamXG.date.desc()).limit(5).all()

        wins = sum(1 for m in recent if (
            (m.home_team == team_name and m.home_goals > m.away_goals) or
            (m.away_team == team_name and m.away_goals > m.home_goals)
        ))
        draws = sum(1 for m in recent if m.home_goals == m.away_goals)

        return {
            "is_home": 1 if is_home else 0,
            "avg_xg_for":   np.mean([x.xg_for for x in xg_records]) if xg_records else 1.5,
            "avg_xg_ag":    np.mean([x.xg_against for x in xg_records]) if xg_records else 1.5,
            "avg_goals_for": np.mean([x.goals_for for x in xg_records]) if xg_records else 1.5,
            "avg_goals_ag":  np.mean([x.goals_against for x in xg_records]) if xg_records else 1.5,
            "wins_last5":   wins,
            "draws_last5":  draws,
        }

    home_feats = get_team_features(home, True, db)
    X = np.array([[home_feats[k] for k in
                   ["is_home","avg_xg_for","avg_xg_ag","avg_goals_for","avg_goals_ag","wins_last5","draws_last5"]]])

    probs = MODEL.predict_proba(X)[0]
    classes = LE.classes_  # sorted alphabetically: D, L, W
    result = dict(zip(classes, [round(float(p)*100, 1) for p in probs]))

    return {
        "home": home, "away": away,
        "probabilities": {
            "home_win": result.get("W", 0),
            "draw":     result.get("D", 0),
            "away_win": result.get("L", 0),
        }
    }
