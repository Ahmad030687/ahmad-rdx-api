from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os
import base64
import random

app = Flask(__name__)

# --- RDX INTELLIGENT AGENTS ---
# Facebook ko pagal banane ke liye alag alag mobile agents
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
]

@app.route('/')
def home():
    return "🦅 AHMAD RDX API - SYSTEM LIVE (Safe Mode)"

@app.route('/ahmad-dl')
def get_info():
    url = request.args.get('url')
    if not url: 
        return jsonify({"status": False, "msg": "Link missing"})
    
    # Random User Agent Select Karen
    current_agent = random.choice(USER_AGENTS)
    
    # --- RDX OPTIMIZED SETTINGS ---
    ydl_opts = {
        'format': 'best',  # Best quality
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,  # Error par crash na ho
        'nocheckcertificate': True, # SSL Errors bypass
        
        # 🔥 Sabse Important: Cookies File
        'cookiefile': 'cookies.txt', 
        
        # 🔥 Facebook ko Mobile ban kar request bhejo
        'user_agent': current_agent,
        
        # 🔥 Geo-Bypass & Mobile Headers
        'geo_bypass': True,
        'extractor_args': {
            'facebook': {
                'mobile': ['true'] # Force mobile version (Facebook mobile pe security kam rakhta hai)
            }
        },
        'http_headers': {
            'Referer': 'https://m.facebook.com/',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Info Extract Karen
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return jsonify({"status": False, "msg": "Video extract nahi ho saki (Cookies Expired?)"})

            real_url = info.get('url')
            title = info.get('title', 'Facebook Video')
            
            if not real_url:
                return jsonify({"status": False, "msg": "Direct URL nahi mila"})
            
            # Base64 Encode (Link ko safe rakhne ke liye)
            token = base64.b64encode(real_url.encode('ascii')).decode('ascii')
            
            # Proxy Link Generate Karen
            final_link = f"{request.host_url}proxy-dl?token={token}"
            
            return jsonify({
                "status": True,
                "title": title,
                "url": final_link,
                "quality": "HD/SD"
            })

    except Exception as e:
        error_msg = str(e)
        print(f"Server Error: {error_msg}")
        
        if "Sign in" in error_msg or "registered users" in error_msg:
            return jsonify({"status": False, "msg": "Cookies Expired! Please update cookies.txt"})
            
        return jsonify({"status": False, "msg": "Facebook Security High Hai, Dubara Try Karen."})

@app.route('/proxy-dl')
def proxy_dl():
    token = request.args.get('token')
    if not token: 
        return Response("No token provided", status=400)

    try:
        # Asli URL wapis nikalein
        target_url = base64.b64decode(token.encode('ascii')).decode('ascii')
        
        # Streaming ke liye headers
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://www.facebook.com/"
        }

        # Video Stream Karen (Memory Full nahi hogi)
        req = requests.get(target_url, headers=headers, stream=True, timeout=30)
        
        return Response(
            req.iter_content(chunk_size=1024*1024), 
            content_type=req.headers.get('Content-Type', 'video/mp4')
        )

    except Exception as e:
        return Response(f"Streaming Error: {str(e)}", status=500)

if __name__ == "__main__":
    # Render Port settings
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
