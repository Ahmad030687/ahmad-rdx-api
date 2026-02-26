from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
import os

app = Flask(__name__)

# 🔑 Gemini API Key (AI Studio se free milti hai)
GEMINI_API_KEY = "AIzaSyCFlf6SQY9PcqHp-1hG7b26o5TrH-XT2cI"
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/rdx/edit', methods=['GET'])
def edit_image():
    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')
    api_key = request.args.get('apikey')

    if api_key != "AhmadRDX":
        return jsonify({"success": False, "error": "Wrong API Key"}), 403

    try:
        # 1. Image Download karna
        img_data = requests.get(image_url).content
        
        # 2. Gemini 1.5 Flash Model (Fast & Low RAM)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. AI ko Image aur Prompt bhejna
        # Note: Gemini 1.5 Flash image ko "samajh" kar naya vision de sakta hai
        response = model.generate_content([
            f"Act as NanoBanana AI. Edit this image based on this prompt: {prompt}. If you can't edit directly, describe exactly how the edited version should look.",
            {"mime_type": "image/jpeg", "data": img_data}
        ])

        return jsonify({
            "success": True,
            "data": {
                "result": {
                    "text": response.text,
                    "url": image_url # Yahan hum image generation API ka link add kar sakte hain
                }
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
