import os
from flask import Flask, render_template, jsonify, request
from groq import Groq
from dotenv import load_dotenv

# Configuración básica
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Conexión con la IA
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    print("✅ CEREBRO CONECTADO A GROQ")
except:
    print("❌ ERROR: No encuentro la API KEY")

state = {
    "avg_mood": 0.5,
    "videos": [
        {"id": 1, "humia": "Lumen", "level": 1, "xp": 0, "path": "https://assets.mixkit.co/videos/preview/mixkit-abstract-digital-technology-background-render-43515-large.mp4", "text": "Esperando input..."},
        {"id": 2, "humia": "Orbital", "level": 1, "xp": 0, "path": "https://assets.mixkit.co/videos/preview/mixkit-stars-in-space-background-1610-large.mp4", "text": "Sistemas en línea."}
    ]
}

@app.route('/')
def home():
    return render_template('index.html', videos=state["videos"], avg_mood=state["avg_mood"])

@app.route('/oracle', methods=['POST'])
def oracle():
    pregunta = request.json.get("question", "")
    print(f"🔮 Pregunta recibida: {pregunta}") # Esto saldrá en la terminal
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Eres el Oráculo de Humia. Tus respuestas son místicas, profundas y analíticas sobre la convergencia biológico-digital."},
                {"role": "user", "content": pregunta}
            ],
            # Actualizamos al modelo más potente y actual:
            model="llama-3.3-70b-versatile", 
            temperature=0.8,
        )
        respuesta = completion.choices[0].message.content
        return jsonify({"responses": {"Oráculo": respuesta}})
    except Exception as e:
        return jsonify({"responses": {"Oráculo": f"Error de conexión: {str(e)}"}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)