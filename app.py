from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os

app = Flask(__name__)

@app.get('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐏𝐘𝐓𝐇𝐎𝐍 - Ultra Stable"

@app.route('/ahmad-dl')
def download_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False})
    
    ydl_opts = {
        'format': 'best', 'quiet': True, 'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Hum bot ko ab direct proxy wala link denge
            proxy_url = f"{request.host_url}proxy-dl?url={info.get('url')}"
            return jsonify({
                "status": True,
                "title": info.get('title', 'Social Video'),
                "url": proxy_url, # Bot ab is proxy link ko use karega
                "headers": info.get('http_headers', {})
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# 🛡️ TikTok 403 Bypass Engine: Ye video ko stream karega
@app.route('/proxy-dl')
def proxy_dl():
    target_url = request.args.get('url')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/'
    }
    r = requests.get(target_url, headers=headers, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type=r.headers['Content-Type'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
