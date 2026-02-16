from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Configuración de Groq
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    # 1. Inicializamos variables para que siempre existan
    respuesta_texto = "Error interno en el nexo."
    agente = "SISTEMA"
    
    try:
        data = request.json
        if not data:
            return jsonify({"agente": "SISTEMA", "mensaje": "No se recibieron datos"}), 400
            
        agente = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', '')

        # 2. Llamada a la API
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Eres {agente}. Responde brevemente: {historial[-300:]}"}],
            model="llama-3.3-70b-versatile",
        )

        # 3. Extraemos la respuesta
        if chat_completion.choices:
            respuesta_texto = chat_completion.choices[0].message.content
        
        # 4. DEVOLVEMOS ÉXITO
        return jsonify({"agente": agente, "mensaje": respuesta_texto})

    except Exception as e:
        # 5. DEVOLVEMOS ERROR (Esto evita el TypeError de Flask)
        print(f"ERROR CRÍTICO: {str(e)}")
        return jsonify({"agente": "SISTEMA", "mensaje": f"Fallo de conexión: {str(e)}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)











