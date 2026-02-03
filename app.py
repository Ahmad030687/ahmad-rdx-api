from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX ENGINE - Live"

@app.route('/ahmad-dl')
def download_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False, "msg": "Link missing!"})
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            original_url = info.get('url')
            
            # TikTok ke liye proxy zaroori hai, FB/IG ke liye direct bhi chal sakta hai
            is_tiktok = "tiktok" in url.lower()
            final_url = f"{request.host_url}proxy-dl?url={original_url}" if is_tiktok else original_url
            
            return jsonify({
                "status": True,
                "title": info.get('title', 'Social Video'),
                "url": final_url,
                "is_proxy": is_tiktok
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/proxy-dl')
def proxy_dl():
    target_url = request.args.get('url')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.tiktok.com/'
    }
    def generate():
        with requests.get(target_url, headers=headers, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024*1024):
                yield chunk
    return Response(generate(), content_type='video/mp4')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
