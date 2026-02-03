from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - TIKTOK SPECIAL"

@app.route('/ahmad-dl')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False, "msg": "Link missing"})
    
    # TikTok ke liye best settings
    ydl_opts = {
        'format': 'best', # Best quality
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 10, # Jaldi connect karo
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            real_url = info.get('url')
            
            # 🛡️ Link ko Base64 mein badal rahe hain taake toote nahi
            token = base64.b64encode(real_url.encode('ascii')).decode('ascii')
            
            # Agar Headers
            
