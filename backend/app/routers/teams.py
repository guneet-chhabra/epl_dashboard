from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/")
def get_all_teams(db: Session = Depends(get_db)):
    teams = db.query(models.TeamXG.team).distinct().all()
    return sorted([t[0] for t in teams])

@router.get("/{team_name}/xg")
def get_team_xg(team_name: str, db: Session = Depends(get_db)):
    # Try exact match first, then try with FC appended
    records = db.query(models.TeamXG).filter(
        models.TeamXG.team == team_name
    ).order_by(models.TeamXG.date).all()
    
    if not records:
        records = db.query(models.TeamXG).filter(
            models.TeamXG.team == team_name + " FC"
        ).order_by(models.TeamXG.date).all()
    
    return records

@router.get("/{team_name}/form")
def get_team_form(team_name: str, db: Session = Depends(get_db)):
    # Match table uses names without FC — strip it for matching
    clean_name = team_name.replace(" FC", "").strip()
    
    # Try several name variations since API and Understat use different formats
    name_variants = [
        clean_name,
        team_name,
        clean_name + " City",
        clean_name.replace("Wolverhampton Wanderers", "Wolverhampton Wanderers"),
    ]
    
    # Build a flexible search
    from sqlalchemy import or_
    matches = db.query(models.Match).filter(
        or_(
            models.Match.home_team.ilike(f"%{clean_name}%"),
            models.Match.away_team.ilike(f"%{clean_name}%"),
        ),
        models.Match.status == "FINISHED"
    ).order_by(models.Match.date.desc()).limit(10).all()

    results = []
    for m in matches:
        is_home = clean_name.lower() in m.home_team.lower()
        if is_home:
            if m.home_goals > m.away_goals:    r = "W"
            elif m.home_goals == m.away_goals:  r = "D"
            else:                               r = "L"
        else:
            if m.away_goals > m.home_goals:    r = "W"
            elif m.away_goals == m.home_goals:  r = "D"
            else:                              r = "L"
        results.append({
            "date":   str(m.date),
            "result": r,
            "home":   m.home_team,
            "away":   m.away_team,
            "score":  f"{m.home_goals}-{m.away_goals}"
        })
    return results