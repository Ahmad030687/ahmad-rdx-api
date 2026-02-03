from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os
import base64 # 🛡️ Ye hai wo tool jo link ko tootne se bachayega

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX ENGINE - BASE64 MODE"

@app.route('/ahmad-dl')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False, "msg": "Link missing"})
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # iPhone User-Agent taake TikTok ko lage mobile hai
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile Safari/604.1'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            real_url = info.get('url')
            
            # 🛡️ STEP 1: Link ko Base64 mein convert karna (Taake toote nahi)
            url_bytes = real_url.encode('ascii')
            base64_bytes = base64.b64encode(url_bytes)
            base64_url = base64_bytes.decode('ascii')
            
            # Ab hum ye safe Base64 string bhejenge
            proxy_link = f"{request.host_url}proxy-dl?token={base64_url}"
            
            return jsonify({
                "status": True,
                "title": info.get('title', 'Social Video'),
                "url": proxy_link,
                "is_proxy": True
            })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/proxy-dl')
def proxy_dl():
    token = request.args.get('token')
    if not token: return Response("Error: No token", status=400)

    try:
        # 🛡️ STEP 2: Wapis Original URL nikalna
        base64_bytes = token.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        target_url = message_bytes.decode('ascii')
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile Safari/604.1",
            "Referer": "https://www.tiktok.com/"
        }

        def generate():
            # 120s Timeout taake bari video bhi download ho jaye
            with requests.get(target_url, headers=headers, stream=True, timeout=120) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024 * 1024): # 1MB chunks
                    yield chunk

        return Response(generate(), content_type="video/mp4")

    except Exception as e:
        return Response(f"Proxy Error: {str(e)}", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
