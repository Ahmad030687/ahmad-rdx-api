from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import json
import random
import time

app = Flask(__name__)
CORS(app)

API_KEY = "AhmadRDX"
CREATOR = "AHMAD RDX"

COOKIE_JSON = "cookie.json"
COOKIE_FILE = "cookies.txt"

# 🔥 Huge Proxy Pool (Rotate)
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
"http://167.172.238.6:10004",
"http://142.93.223.221:80",
"http://134.209.29.120:3128",
"http://68.183.143.134:80",
"http://45.77.248.114:80",
"http://45.76.177.29:8080",
"http://165.22.254.253:80"
]


# 🔥 JSON → Netscape Converter
def convert_json_to_netscape(json_cookies):
    lines = [
        "# Netscape HTTP Cookie File",
        "# This file was generated automatically\n"
    ]

    for cookie in json_cookies:
        domain = cookie.get("domain", "")
        include_sub = "TRUE" if domain.startswith(".") else "FALSE"
        path = cookie.get("path", "/")
        secure = "TRUE" if cookie.get("secure", False) else "FALSE"
        expiry = str(int(cookie.get("expirationDate", 0)))
        name = cookie.get("name", "")
        value = cookie.get("value", "")

        line = f"{domain}\t{include_sub}\t{path}\t{secure}\t{expiry}\t{name}\t{value}"
        lines.append(line)

    return "\n".join(lines)


# 🔥 Load Cookies (if cookie.json exists)
def load_cookies():
    try:
        if not os.path.exists(COOKIE_JSON):
            return False

        with open(COOKIE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        cookies = data.get("cookies", [])
        if not cookies:
            return False

        netscape = convert_json_to_netscape(cookies)
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            f.write(netscape)

        return True
    except Exception as e:
        print("Cookie Load Error:", e)
        return False


# 🔥 Proxy Selector
def get_proxy():
    return {
        "http": random.choice(PROXIES),
        "https": random.choice(PROXIES)
    }


# 🔥 Multi Extractor (Best Effort)
def extract_with_yt_dlp(url):
    ydl_opts = {
        "format": "best",
        "quiet": True,
        "no_warnings": True,
        "cachedir": False,
        "cookiefile": COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "proxy": random.choice(PROXIES)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("url")
    except Exception:
        return None


# 🔥 Fallback Extractor (Second Attempt)
def extract_with_fallback(url):
    try:
        options = {
            "format": "best",
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("url")
    except Exception:
        return None


# 🔥 Final Extraction (Multi Layer)
def get_video_info(url):
    for attempt in range(3):  # 3 retries
        try:
            # Try main extractor
            video_url = extract_with_yt_dlp(url)

            # If fail, try fallback
            if not video_url:
                video_url = extract_with_fallback(url)

            if video_url:
                return {
                    "status": True,
                    "statusCode": 200,
                    "creator": CREATOR,
                    "input": url,
                    "result": {
                        "video": video_url
                    }
                }

        except Exception:
            time.sleep(2)
            continue

    return {"status": False, "error": "Extraction failed"}


@app.route('/')
def home():
    return jsonify({
        "message": "🦅 Multi Extractor API Running",
        "usage": "/downloader/aiodl?apikey=AhmadRDX&url=LINK"
    })


@app.route('/downloader/aiodl', methods=['GET'])
def downloader():
    url = request.args.get('url')
    apikey = request.args.get('apikey')

    if apikey != API_KEY:
        return jsonify({"status": False, "msg": "Invalid API Key"}), 403

    if not url:
        return jsonify({"status": False, "msg": "URL missing"}), 400

    load_cookies()

    result = get_video_info(url)
    return jsonify(result)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
