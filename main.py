from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "message": "YouTube Transcript API running... use /transcript/?url=your_video_url",
            "creator": "Sujan rai"
        }
    )

@app.get("/transcript/")
async def get_transcript(url: str = Query(None, description="YouTube video URL")):
    if not url or url.strip() == "":
        return JSONResponse(
            content={
                "success": False,
                "error": "please provide a valid YouTube video URL as ?url= parameter."
            }
        )
    try:
        api_url = f"https://socialdown.itz-ashlynn.workers.dev/yt-trans?url={url}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("success") and data.get("transcript"):
            return JSONResponse(
                content={
                    "success": True,
                    "transcripts": data["transcript"]
                }
            )
        else:
            return JSONResponse(
                content={
                    "success": False,
                    "error": "sorry, check your video URL or no transcripts available."
                }
            )
    except Exception:
        return JSONResponse(
            content={
                "success": False,
                "error": "sorry, check your video URL or no transcripts available."
            }
        )