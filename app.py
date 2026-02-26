from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🍪 AAPKI DI HUI COOKIE (Yahan fit kar di hai)
RDX_COOKIE = "AEC=AVh_V2iyBHpOrwnn7CeXoAiedfWn9aarNoKT20Br2UX9Td9K-RAeS_o7Sg; HSID=Ao0szVfkYnMchTVfk; SSID=AGahZP8H4ni4UpnFV; APISID=SD-Q2DJLGdmZcxlA/AS8N0Gkp_b9sJC84f; SAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-1PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-3PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; SEARCH_SAMESITE=CgQI354B; SID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bZzx09pPfc201wUcRVKfh-wACgYKAXUSARMSFQHGX2MiU_dnPuMOs-717cJlLCeWOBoVAUF8yKpYTllPAbVgYQ0Mr_GyeXxV0076; __Secure-1PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3b_Pt9L1eqcIAVeh7ZdRBOXgACgYKAYESARMSFQHGX2MicAK_Acu_-NCkzEz2wjCHmxoVAUF8yKp9xk8gQ82f-Ob76ysTXojB0076; __Secure-3PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bUudZTunPKtKbLRSoGKl1dAACgYKAYISARMSFQHGX2MimdzCEq63UmiyGU-3eyZx9RoVAUF8yKrc4ycLY7LGaJUyDXk_7u7M0076"

@app.route('/rdx/edit', methods=['GET'])
def nano_banana_edit():
    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')
    api_key = request.args.get('apikey')

    # Security Check
    if api_key != "AhmadRDX":
        return jsonify({"success": False, "error": "Ghalat API Key hai Ahmad bhai!"}), 403

    if not prompt or not image_url:
        return jsonify({"success": False, "error": "Prompt ya Image URL missing hai."}), 400

    try:
        # 🔗 Bridge to NanoBanana Engine
        target_url = "https://anabot.my.id/api/ai/geminiOption"
        
        params = {
            "prompt": prompt,
            "type": "NanoBanana",
            "imageUrl": image_url,
            "cookie": RDX_COOKIE,
            "apikey": "freeApikey"
        }

        headers = {
            "User-Agent": "AHMAD RDX Image Editor/2.0.0",
            "Accept": "application/json"
        }

        # Request bhejna
        response = requests.get(target_url, params=params, headers=headers, timeout=60)
        data = response.json()

        if data.get("success"):
            return jsonify({
                "success": True,
                "author": "AHMAD RDX",
                "result_url": data['data']['result']['url']
            })
        else:
            return jsonify({
                "success": False,
                "error": data.get("error", "AI Engine ne response nahi diya.")
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
