from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.database import Base

class Team(Base):
    __tablename__ = "teams"
    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String, unique=True, index=True)
    short    = Column(String)       # e.g. "ARS", "MCI"
    stadium  = Column(String)
    manager  = Column(String)

class Match(Base):
    __tablename__ = "matches"
    id           = Column(Integer, primary_key=True)
    matchday     = Column(Integer)
    date         = Column(Date)
    home_team    = Column(String)
    away_team    = Column(String)
    home_goals   = Column(Integer, nullable=True)
    away_goals   = Column(Integer, nullable=True)
    home_xg      = Column(Float, nullable=True)
    away_xg      = Column(Float, nullable=True)
    status       = Column(String)   # FINISHED, SCHEDULED

class Player(Base):
    __tablename__ = "players"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    name           = Column(String)
    team           = Column(String)
    position       = Column(String)
    goals          = Column(Integer, default=0)
    assists        = Column(Integer, default=0)
    xg             = Column(Float, default=0.0)
    xag            = Column(Float, default=0.0)
    key_passes     = Column(Integer, default=0)
    prog_carries   = Column(Integer, default=0)
    matches_played = Column(Integer, default=0)

class TeamXG(Base):
    __tablename__ = "team_xg"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    team        = Column(String)
    date        = Column(Date)
    xg_for      = Column(Float)
    xg_against  = Column(Float)
    goals_for   = Column(Integer)
    goals_against = Column(Integer)
    result      = Column(String)    # W, D, L
    home        = Column(String)    # h or a