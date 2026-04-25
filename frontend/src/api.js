import axios from "axios";

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL });

export const getTeamXG    = (team) => API.get(`/teams/${team}/xg`);
export const getTeamForm  = (team) => API.get(`/teams/${team}/form`);
export const getPlayers   = ()     => API.get(`/players/`);
export const getPlayer    = (id)   => API.get(`/players/${id}`);
export const predictMatch = (home, away) =>
  API.get(`/matches/predict?home=${home}&away=${away}`);