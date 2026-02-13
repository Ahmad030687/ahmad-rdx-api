from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "owner": "AHMAD RDX", "msg": "RDX API Store Live"}

# Ye hai AIODL ka rasta
@app.get("/api/aiodl")
def aiodl(url: str = Query(..., description="Yahan link paste karein")):
    try:
        # ⚙️ yt-dlp Settings (Video nikalne ka engine)
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Step 1: Link se data nikalna
            info = ydl.extract_info(url, download=False)
            
            # Step 2: Result wapas bhejna
            return {
                "status": True,
                "creator": "AHMAD RDX",
                "result": {
                    "title": info.get('title', 'No Title'),
                    "platform": info.get('extractor_key'),
                    "url": info.get('url'), # Ye direct video link hai
                    "thumbnail": info.get('thumbnail')
                }
            }
    except Exception as e:
        return {"status": False, "error": str(e)}
        
