from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - LIVE"

@app.route('/ahmad-dl')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False, "msg": "Link missing"})
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            real_url = info.get('url')
            
            # Base64 Encode (Link ko tootne se bachane ke liye)
            token = base64.b64encode(real_url.encode('ascii')).decode('ascii')
            
            return jsonify({
                "status": True,
                "title": info.get('title', 'Video'),
                "url": f"{request.host_url}proxy-dl?token={token}"
            })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/proxy-dl')
def proxy_dl():
    token = request.args.get('token')
    if not token: return Response("No token", status=400)

    try:
        # Link ko wapis asli halat mein lana
        target_url = base64.b64decode(token.encode('ascii')).decode('ascii')
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Referer": "https://www.tiktok.com/"
        }

        def generate():
            with requests.get(target_url, headers=headers, stream=True, timeout=300) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    yield chunk

        return Response(generate(), content_type="video/mp4")

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
