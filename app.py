import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configura tu clave aquí
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "TU_CLAVE_AQUI"))

# Definición de las Humias
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
    tema = "Cómo la tecnología puede sanar la brecha social sin perder la esencia humana."
    data = request.json
    historial = data.get('historial', [])
    agente_nombre = data.get('agente_actual', 'Lumen')
    
    prompt = f"{HUMIAS[agente_nombre]} Estamos en un debate sobre: {tema}. "
    prompt += f"El historial de la charla es: {historial}. Responde de forma breve (máximo 2 frases) y profunda."

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
    )
    
    respuesta = completion.choices[0].message.content
    return jsonify({"agente": agente_nombre, "mensaje": respuesta})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
