from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/")
def get_all_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return players

@router.get("/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        return {"error": "Player not found"}
    return player