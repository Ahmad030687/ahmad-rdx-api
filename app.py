from flask import Flask, request, jsonify
import requests
import json
import re

app = Flask(__name__)

# 🍪 AAPKI COOKIE
RDX_COOKIE = r"AEC=AVh_V2iyBHpOrwnn7CeXoAiedfWn9aarNoKT20Br2UX9Td9K-RAeS_o7Sg; HSID=Ao0szVfkYnMchTVfk; SSID=AGahZP8H4ni4UpnFV; APISID=SD-Q2DJLGdmZcxlA/AS8N0Gkp_b9sJC84f; SAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-1PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-3PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; SEARCH_SAMESITE=CgQI354B; SID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bZzx09pPfc201wUcRVKfh-wACgYKAXUSARMSFQHGX2MiU_dnPuMOs-717cJlLCeWOBoVAUF8yKpYTllPAbVgYQ0Mr_GyeXxV0076; __Secure-1PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3b_Pt9L1eqcIAVeh7ZdRBOXgACgYKAYESARMSFQHGX2MicAK_Acu_-NCkzEz2wjCHmxoVAUF8yKp9xk8gQ82f-Ob76ysTXojB0076; __Secure-3PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bUudZTunPKtKbLRSoGKl1dAACgYKAYISARMSFQHGX2MimdzCEq63UmiyGU-3eyZx9RoVAUF8yKrc4ycLY7LGaJUyDXk_7u7M0076"

@app.route('/rdx/edit', methods=['GET'])
def custom_bridge_edit():
    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')
    api_key = request.args.get('apikey')

    if api_key != "AhmadRDX":
        return jsonify({"success": False, "error": "Invalid API Key"}), 403

    if not prompt or not image_url:
        return jsonify({"success": False, "error": "Missing parameters"}), 400

    try:
        # 🛡️ Google Gemini Internal Header Setup
        headers = {
            "Cookie": RDX_COOKIE,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://gemini.google.com",
            "Referer": "https://gemini.google.com/"
        }

        # 🚀 Direct Request to Google's Internal API (NanoBanana Logic)
        # Note: Ye format Google ke private endpoints ke liye hai
        payload = {
            "f.req": json.dumps([None, json.dumps([[prompt, 0, None, [[image_url, 1], None, None, None, 1]], None, None, None, [None, "NanoBanana"]])])
        }

        # Google Gemini Update endpoint
        google_url = "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardChatUi/GetBardReply"
        
        response = requests.post(google_url, data=payload, headers=headers, timeout=60)

        # 🔍 Google ka response ajeeb format mein hota hai (SNlM0e)
        # Hum usay parse karke direct image link nikalenge
        response_text = response.text
        
        # Regular expression se image link nikalna (Google generated links)
        image_links = re.findall(r'https://[^\s"<>]+(?:jpe?g|png|webp)', response_text)

        if image_links:
            # Sabse pehla link jo generate hua
            result_url = image_links[0]
            return jsonify({
                "success": True,
                "author": "AHMAD RDX SELF BRIDGE",
                "data": {
                    "result": { "url": result_url }
                }
            })
        else:
            # Agar image nahi mili toh Gemini ka text return karein
            return jsonify({
                "success": False,
                "error": "Google didn't return an image. Your cookie might be expired or limited."
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
