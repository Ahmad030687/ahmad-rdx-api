from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐏𝐘𝐓𝐇𝐎𝐍 - Universal DL is Live!"

@app.route('/rdx-dl')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": False, "msg": "Link missing Ahmad bhai!"})

    try:
        # yt-dlp ki settings (Sirf URL nikalne ke liye)
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
            
            if video_url:
                return jsonify({
                    "status": True,
                    "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗",
                    "title": info.get('title', 'Video'),
                    "url": video_url
                })
            else:
                return jsonify({"status": False, "msg": "Video URL not found!"})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
