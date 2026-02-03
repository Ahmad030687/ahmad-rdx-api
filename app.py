from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os
from urllib.parse import quote, unquote  # 🛡️ Ye library link ko tootne se bachayegi

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX FINAL ENGINE - LIVE"

@app.route('/ahmad-dl')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False, "msg": "Link missing"})
    
    # 📱 iPhone User-Agent (TikTok isey kabhi block nahi karta)
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile Safari/604.1'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            real_video_url = info.get('url')
            
            # 🛡️ MAIN FIX: Link ko 'Lock' (Encode) kar rahe hain taake wo toote nahi
            # Pehle ye 'https://tiktok.com?a=1&b=2' tha (jo toot jata tha)
            # Ab ye 'https%3A%2F%2Ftiktok.com%3Fa%3D1%26b%3D2' ban jayega (Safe)
            safe_url = quote(real_video_url)
            
            # Ab hum bot ko wo link denge jo hamare proxy se guzre ga
            proxy_link = f"{request.host_url}proxy-dl?url={safe_url}"
            
            return jsonify({
                "status": True,
                "title": info.get('title', 'Social Video'),
                "url": proxy_link,  # Bot ko ye wala link milega
                "is_proxy": True
            })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/proxy-dl')
def proxy_dl():
    # Jab Bot wapis aayega, hum link ko wapis 'Unlock' (Decode) nahi karenge
    # Kyunke Flask automatically decode kar deta hai request.args mein.
    target_url = request.args.get('url')
    
    if not target_url: 
        return Response("No URL provided", status=400)

    # Headers taake TikTok ko lage ke iPhone se request aa rahi hai
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile Safari/604.1",
        "Referer": "https://www.tiktok.com/"
    }
    
    def generate():
        try:
            # Stream=True zaroori hai bari videos ke liye
            with requests.get(target_url, headers=headers, stream=True, timeout=60) as r:
                r.raise_for_status() # Agar 403/404 aaya to yahan error pakra jayega
                for chunk in r.iter_content(chunk_size=1024 * 1024): # 1MB Chunks
                    yield chunk
        except Exception as e:
            print(f"Proxy Error: {e}")

    return Response(generate(), content_type="video/mp4")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
