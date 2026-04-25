from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/")
def get_all_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams

@router.get("/{team_name}/xg")
def get_team_xg(team_name: str, db: Session = Depends(get_db)):
    records = db.query(models.TeamXG).filter(
        models.TeamXG.team == team_name
    ).order_by(models.TeamXG.date).all()
    return records

@router.get("/{team_name}/form")
def get_team_form(team_name: str, db: Session = Depends(get_db)):
    # Last 10 matches for this team (home or away)
    from sqlalchemy import or_
    matches = db.query(models.Match).filter(
        or_(models.Match.home_team == team_name,
            models.Match.away_team == team_name),
        models.Match.status == "FINISHED"
    ).order_by(models.Match.date.desc()).limit(10).all()
    
    results = []
    for m in matches:
        if m.home_team == team_name:
            if m.home_goals > m.away_goals: r = "W"
            elif m.home_goals == m.away_goals: r = "D"
            else: r = "L"
        else:
            if m.away_goals > m.home_goals: r = "W"
            elif m.away_goals == m.home_goals: r = "D"
            else: r = "L"
        results.append({"date": str(m.date), "result": r,
                        "home": m.home_team, "away": m.away_team,
                        "score": f"{m.home_goals}-{m.away_goals}"})
    return results