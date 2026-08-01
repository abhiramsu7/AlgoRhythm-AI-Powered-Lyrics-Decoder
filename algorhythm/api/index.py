from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import lyricsgenius
from google import genai

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENIUS_TOKEN = os.environ.get("GENIUS_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genius = lyricsgenius.Genius(GENIUS_TOKEN) if GENIUS_TOKEN else None
client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

@app.get("/api/health")
def check_health():
    return {"status": "AlgoRhythm Engine Online"}

@app.get("/api/search")
def search_tracks(q: str = Query(..., min_length=2)):
    """Fetches real-time song suggestions as the user types."""
    if not genius:
        return {"results": [], "error": "GENIUS_TOKEN not configured"}
    
    try:
        # Fetch top 5 matching tracks
        res = genius.search_songs(q, per_page=5)
        hits = res.get("hits", [])
        
        results = []
        for hit in hits:
            song_data = hit.get("result", {})
            results.append({
                "id": song_data.get("id"),
                "title": song_data.get("title"),
                "artist": song_data.get("primary_artist", {}).get("name"),
                "art": song_data.get("song_art_image_thumbnail_url")
            })
        return {"results": results}
    except Exception as e:
        return {"results": [], "error": str(e)}