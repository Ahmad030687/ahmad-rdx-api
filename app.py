from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# 🦅 Home Route for Health Check (Prevents 404)
@app.get('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐏𝐘𝐓𝐇𝐎𝐍 𝐄𝐍𝐆𝐈𝐍𝐄 - Status: Ultra Stable"

# 📥 Main Downloader Route
@app.route('/ahmad-dl')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": False, "msg": "Link missing Ahmad bhai!"})

    # 🛡️ Professional yt-dlp Settings
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cachedir': False,
        'nocheckcertificate': True,
        'socket_timeout': 30,
        # TikTok bypass ke liye ye zaroori hai
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Info Extract karna
            info = ydl.extract_info(url, download=False)
            
            # TikTok/FB/IG headers nikalna taake bot download kar sakay
            headers = info.get('http_headers', {})
            
            video_url = info.get('url')
            
            if video_url:
                return jsonify({
                    "status": True,
                    "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗",
                    "title": info.get('title', 'Social Video'),
                    "url": video_url,
                    "headers": headers, # Ye headers bot ko bhej rahe hain
                    "platform": info.get('extractor_key', 'Universal')
                })
            else:
                return jsonify({"status": False, "msg": "Could not find video URL."})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    # Render Port Binding
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
