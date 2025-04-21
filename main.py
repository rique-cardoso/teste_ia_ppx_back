from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/ia": {"origins": "https://rique-cardoso.github.io/"},
})

from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def consultar_gemini(mensagem=""):
    response = model.generate_content(mensagem)
    return response.text

@app.route('/ia', methods=['POST'])
def ia():
    data = request.json
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"erro": "Prompt não fornecido"}), 400
    
    try:
        resposta = consultar_gemini(prompt)
        return jsonify({"resposta": resposta})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run()