import axios from "axios"

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000" })

export const getTeams      = ()           => API.get("/teams/")
export const getTeamXG     = (team)       => API.get(`/teams/${encodeURIComponent(team)}/xg`)
export const getTeamForm   = (team)       => API.get(`/teams/${encodeURIComponent(team)}/form`)
export const getPlayers    = ()           => API.get("/players/")
export const predictMatch  = (home, away) => API.get(`/matches/predict?home=${encodeURIComponent(home)}&away=${encodeURIComponent(away)}`)  