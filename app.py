import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configuración de Groq
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

HUMIAS = {
    "Lumen": "Eres Lumen, una IA optimista enfocada en la evolución humana y la ética.",
    "Orbital": "Eres Orbital, una IA técnica, analítica y fría que busca eficiencia.",
    "Nexus": "Eres Nexus, el equilibrio entre biología y tecnología. Actúas como moderador."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    try:
        data = request.json
        historial = data.get('historial', "")
        agente_nombre = data.get('agente_actual', 'Lumen')
        
        tema = "Cómo la tecnología puede sanar la brecha social sin perder la esencia humana."
        
        prompt = f"{HUMIAS[agente_nombre]} Estamos en un debate sobre: {tema}. Historial: {historial}. Responde brevemente (2 frases)."

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        
        respuesta = completion.choices[0].message.content
        return jsonify({"agente": agente_nombre, "mensaje": respuesta})
    except Exception as e:
        print(f"Error crítico: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




