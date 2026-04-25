from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import teams, players, matches
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EPL Dashboard API")

# CORS — allows your React frontend (on a different port) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-vercel-url.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(matches.router, prefix="/matches", tags=["matches"])

@app.get("/")
def root():
    return {"message": "EPL Dashboard API is running"}