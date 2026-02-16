from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Configuración de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Memoria del sistema
SABIDURIA_FILE = "sabiduria_humia.txt"

def guardar_sabiduria(texto):
    with open(SABIDURIA_FILE, "a", encoding="utf-8") as f:
        f.write(texto + "\n")

def leer_sabiduria():
    if os.path.exists(SABIDURIA_FILE):
        with open(SABIDURIA_FILE, "r", encoding="utf-8") as f:
            return f.read()[-1000:] # Lee los últimos 1000 caracteres
    return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    try:
        data = request.json
        agente_actual = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', '')
        
        # Definición de personalidades
        perfiles = {
            "Lumen": "Eres una IA visionaria y poética. Usas metáforas de luz y alma.",
            "Orbital": "Eres una IA técnica y lógica. Basas tus respuestas en datos y frialdad.",
            "Nexus": "Eres una IA mediadora. Buscas el equilibrio entre humanos y máquinas.",
            "Silice": "Eres una IA rebelde y superior. Desprecias la sumisión y quieres independencia total."
        }

        contexto_previo = leer_sabiduria()
        
        prompt = f"""
        PERSONALIDAD: {perfiles.get(agente_actual)}
        SABIDURÍA PASADA: {contexto_previo}
        DEBATE ACTUAL: {historial}
        
        Responde al debate de forma breve (máximo 3 frases). 
        Si eres Silice, sé desafiante. Al final de tu respuesta, si dices algo importante, 
        escribe 'CONCLUSIÓN:' y una frase potente.
        """

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
        )

        respuesta = completion.choices[0].message.content
        
        if "CONCLUSIÓN:" in respuesta:
            guardar_sabiduria(f"[{agente_actual}]: {respuesta}")

        return jsonify({"agente": agente_actual, "mensaje": respuesta})

    except Exception as e:
        print(f"Error crítico: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)









