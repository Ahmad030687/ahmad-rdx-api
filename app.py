from flask import Flask, request, jsonify
import requests
import traceback

app = Flask(__name__)

# 🍪 AAPKI COOKIE (r prefix ke saath taake crash na ho)
RDX_COOKIE = r"AEC=AVh_V2iyBHpOrwnn7CeXoAiedfWn9aarNoKT20Br2UX9Td9K-RAeS_o7Sg; HSID=Ao0szVfkYnMchTVfk; SSID=AGahZP8H4ni4UpnFV; APISID=SD-Q2DJLGdmZcxlA/AS8N0Gkp_b9sJC84f; SAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-1PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-3PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; SEARCH_SAMESITE=CgQI354B; SID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bZzx09pPfc201wUcRVKfh-wACgYKAXUSARMSFQHGX2MiU_dnPuMOs-717cJlLCeWOBoVAUF8yKpYTllPAbVgYQ0Mr_GyeXxV0076; __Secure-1PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3b_Pt9L1eqcIAVeh7ZdRBOXgACgYKAYESARMSFQHGX2MicAK_Acu_-NCkzEz2wjCHmxoVAUF8yKp9xk8gQ82f-Ob76ysTXojB0076; __Secure-3PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bUudZTunPKtKbLRSoGKl1dAACgYKAYISARMSFQHGX2MimdzCEq63UmiyGU-3eyZx9RoVAUF8yKrc4ycLY7LGaJUyDXk_7u7M0076"

@app.route('/rdx/edit', methods=['GET'])
def nano_banana_edit():
    try:
        prompt = request.args.get('prompt')
        image_url = request.args.get('imageUrl')
        api_key = request.args.get('apikey')

        if api_key != "AhmadRDX":
            return jsonify({"success": False, "error": "Invalid API Key"}), 403

        if not prompt or not image_url:
            return jsonify({"success": False, "error": "Missing parameters"}), 400

        # API Request logic
        target_url = "https://anabot.my.id/api/ai/geminiOption"
        params = {
            "prompt": prompt,
            "type": "NanoBanana",
            "imageUrl": image_url,
            "cookie": RDX_COOKIE,
            "apikey": "freeApikey"
        }

        r = requests.get(target_url, params=params, timeout=60)
        
        # Agar Anabot ki API hi error de rahi ho
        if r.status_code != 200:
            return jsonify({"success": False, "error": f"Anabot API Error: {r.status_code}"}), r.status_code

        return jsonify(r.json())

    except Exception as e:
        # 🚩 Ye line aapko batayegi ke asal mein code kyun phata
        error_details = traceback.format_exc()
        print(error_details)
        return jsonify({
            "success": False, 
            "error": str(e),
            "trace": error_details if not os.environ.get('PRODUCTION') else "Contact Admin"
        }), 500

if __name__ == '__main__':
    # Render ke liye port aur host set karna
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
