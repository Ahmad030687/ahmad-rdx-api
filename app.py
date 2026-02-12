from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os
import base64
import json
import time

app = Flask(__name__)

# ==========================================
# 🍪 CORRECTED JSON COOKIES FOR PYTHON
# ==========================================
RAW_JSON_COOKIES = [
    {"domain": ".facebook.com", "expirationDate": 1804001781.765706, "hostOnly": False, "httpOnly": True, "name": "sb", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "lbsxaQTS295Ois2srigFcejO"},
    {"domain": ".facebook.com", "expirationDate": 1803715172.056745, "hostOnly": False, "httpOnly": True, "name": "ps_l", "path": "/", "sameSite": "lax", "secure": True, "session": False, "storeId": "0", "value": "1"},
    {"domain": ".facebook.com", "expirationDate": 1803715172.056848, "hostOnly": False, "httpOnly": True, "name": "ps_n", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "1"},
    {"domain": ".facebook.com", "expirationDate": 1800977781.765431, "hostOnly": False, "httpOnly": False, "name": "c_user", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "61578529016791"},
    {"domain": ".facebook.com", "expirationDate": 1800977781.765839, "hostOnly": False, "httpOnly": True, "name": "xs", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "29%3A5VqxRoDctGchbg%3A2%3A1769441778%3A-1%3A-1"},
    {"domain": ".facebook.com", "expirationDate": 1805498347.876131, "hostOnly": False, "httpOnly": True, "name": "datr", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "T-V4aTWiymScbJLTq-l3p7H8"},
    {"domain": ".facebook.com", "expirationDate": 1805498346.29123, "hostOnly": False, "httpOnly": True, "name": "pas", "path": "/", "sameSite": "lax", "secure": True, "session": False, "storeId": "0", "value": "61559731610845%3ApoLA8U6xwi%2C61564574314688%3AtTafsRuf0A%2C61578529016791%3AQOZE8DZRv1"},
    {"domain": ".facebook.com", "expirationDate": 1776122347, "hostOnly": False, "httpOnly": False, "name": "vpd", "path": "/", "sameSite": "lax", "secure": True, "session": False, "storeId": "0", "value": "v1%3B708x360x3"},
    {"domain": ".facebook.com", "expirationDate": 1771515651.662064, "hostOnly": False, "httpOnly": False, "name": "locale", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "en_US"},
    {"domain": ".facebook.com", "expirationDate": 1778714346.291127, "hostOnly": False, "httpOnly": True, "name": "fr", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "0NmFFZJMeRIr9Kx2t.AWeyogoZa2Mrp3RHAjRvmC5ehaITiNZebjFVEEOkRXNpTmPFcNQ.BpMbuV..AAA.0.0.Bpjl_q.AWdxORasg8oQOJTznvQJQoMDUIQ"},
    {"domain": ".facebook.com", "expirationDate": 1802474347, "hostOnly": False, "httpOnly": False, "name": "fbl_st", "path": "/", "sameSite": "strict", "secure": True, "session": False, "storeId": "0", "value": "100734125%3BT%3A29515639"},
    {"domain": ".facebook.com", "expirationDate": 1778714347, "hostOnly": False, "httpOnly": False, "name": "wl_cbv", "path": "/", "sameSite": "no_restriction", "secure": True, "session": False, "storeId": "0", "value": "v2%3Bclient_version%3A3084%3Btimestamp%3A1770938346"}
]
# ==========================================

def save_cookies():
    """JSON ko Netscape format mein badal kar cookies.txt banana"""
    with open("cookies.txt", "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in RAW_JSON_COOKIES:
            domain = cookie.get('domain', '')
            # True/False for subdomain access
            flag = "TRUE" if domain.startswith('.') else "FALSE"
            path = cookie.get('path', '/')
            secure = "TRUE" if cookie.get('secure', False) else "FALSE"
            expiry = int(cookie.get('expirationDate', time.time() + 3600))
            name = cookie.get('name', '')
            value = cookie.get('value', '')
            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")

@app.route('/')
def home():
    return "🦅 AHMAD RDX - PRIVATE SERVER LIVE (Fixed Cookies Mode)"

@app.route('/ahmad-dl')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({"status": False, "msg": "Link missing"})
    
    # Refresh cookies.txt on every request to be safe
    save_cookies()
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'extractor_args': {'facebook': {'mobile': ['true']}}
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            real_url = info.get('url')
            
            # Base64 for safe transmission
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
    
    target_url = base64.b64decode(token.encode('ascii')).decode('ascii')
    
    def generate():
        # Requests stream taake server load na ho
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        with requests.get(target_url, stream=True, headers=headers) as r:
            for chunk in r.iter_content(chunk_size=1024*1024):
                yield chunk
    return Response(generate(), content_type="video/mp4")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
