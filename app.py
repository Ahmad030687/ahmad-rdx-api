from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# 🦅 RDX CONFIG
API_KEY = "AhmadRDX" # Aapka Secret API Key
CREATOR = "AHMAD RDX"

def get_video_info(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cachedir': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            # Format the response like Koja API
            return {
                "status": True,
                "statusCode": 200,
                "creator": CREATOR,
                "input": url,
                "result": {
                    "extractor": info.get('extractor_key', 'universal'),
                    "title": info.get('title', 'RDX Video'),
                    "thumbnail": info.get('thumbnail', ''),
                    "duration": info.get('duration_string', '00:00'),
                    "links": {
                        "video": [
                            {
                                "resolution": info.get('resolution', 'HD'),
                                "ext": info.get('ext', 'mp4'),
                                "url": info.get('url', '')
                            }
                        ]
                    }
                }
            }
        except Exception as e:
            return {"status": False, "error": str(e)}

@app.route('/')
def home():
    return jsonify({
        "message": "🦅 AHMAD RDX Universal API is Running!",
        "usage": "/downloader/aiodl?apikey=AhmadRDX&url=LINK"
    })

@app.route('/downloader/aiodl', methods=['GET'])
def downloader():
    url = request.args.get('url')
    apikey = request.args.get('apikey')

    # 🛡️ Security Check
    if apikey != API_KEY:
        return jsonify({"status": False, "msg": "Invalid API Key! Ahmad bhai se permission lo."}), 403

    if not url:
        return jsonify({"status": False, "msg": "URL kahan hai Ahmad bhai?"}), 400

    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    # Render/Vercel ke liye port setup
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
