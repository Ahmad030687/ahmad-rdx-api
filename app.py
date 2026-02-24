from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import random
import time

app = Flask(__name__)
CORS(app)

API_KEY = "AhmadRDX"
CREATOR = "AHMAD RDX"

# 🔥 Huge Proxy Pool (production)
PROXIES = [
"http://103.152.112.145:80",
"http://103.152.112.162:80",
"http://103.152.112.195:80",
"http://51.15.242.202:8888",
"http://51.75.206.209:80",
"http://195.154.43.28:3128",
"http://91.107.177.3:80",
"http://103.146.170.252:83",
"http://103.105.40.242:16538",
"http://103.163.51.254:80",
"http://188.166.56.246:80",
"http://178.62.193.19:8080",
"http://159.65.69.186:9300",
"http://167.172.238.6:10004"
]


# 🔥 Multi Extractor (Strong)
def get_video_info(url):
    options = {
        "format": "best",
        "quiet": True,
        "no_warnings": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        }
    }

    # Try multiple times (high success)
    for attempt in range(3):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

                return {
                    "status": True,
                    "creator": CREATOR,
                    "result": {
                        "video": info.get("url"),
                        "title": info.get("title")
                    }
                }

        except Exception:
            time.sleep(2)
            continue

    return {"status": False, "error": "Extraction failed"}


@app.route('/downloader/aiodl', methods=['GET'])
def downloader():
    url = request.args.get('url')
    apikey = request.args.get('apikey')

    if apikey != API_KEY:
        return jsonify({"status": False, "msg": "Invalid API Key"}), 403

    if not url:
        return jsonify({"status": False, "msg": "URL missing"}), 400

    return jsonify(get_video_info(url))


@app.route('/')
def home():
    return jsonify({
        "message": "Multi Downloader API Running",
        "usage": "/downloader/aiodl?apikey=AhmadRDX&url=LINK"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
