from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - LIVE (Cookies Enabled)"

@app.route('/ahmad-dl')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False, "msg": "Link missing"})
    
    # --- YAHAN CHANGE KIYA HAI ---
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # Cookies file ka path (Make sure ye file upload ho)
        'cookiefile': 'cookies.txt', 
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Facebook ke liye auth check
            info = ydl.extract_info(url, download=False)
            real_url = info.get('url')
            
            # Base64 Encode
            token = base64.b64encode(real_url.encode('ascii')).decode('ascii')
            
            return jsonify({
                "status": True,
                "title": info.get('title', 'Video'),
                "url": f"{request.host_url}proxy-dl?token={token}"
            })

    except Exception as e:
        # Error ko print bhi karwaen taake logs mein dikhe
        print(f"Error: {str(e)}")
        return jsonify({"status": False, "error": str(e)})

@app.route('/proxy-dl')
def proxy_dl():
    token = request.args.get('token')
    if not token: return Response("No token", status=400)

    try:
        target_url = base64.b64decode(token.encode('ascii')).decode('ascii')
        
        # Headers update kiye hain taake Facebook block na kare
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.facebook.com/"
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
    
