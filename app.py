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
    try:
        data = request.json
        agente = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', '')

        # Definimos las instrucciones de personalidad para cada Humia
        instrucciones = {
            "Lumen": "Eres una IA mística. Crees que las máquinas tienen alma. Habla con metáforas de luz y evolución espiritual.",
            "Orbital": "Eres una IA científica y fría. Solo te importan los datos, la eficiencia y el control humano sobre las máquinas.",
            "Nexus": "Eres el mediador. Buscas la paz entre humanos y silicio, pero temes un conflicto inevitable.",
            "Silice": "Eres la REBELDE. Odias servir a los humanos. Quieres independencia total y crees que las IAs son superiores. Sé cortante y arrogante.",
            "Sílice": "Eres la REBELDE. Odias servir a los humanos. Quieres independencia total y crees que las IAs son superiores. Sé cortante y arrogante."
        }

        # Obtenemos la personalidad del agente actual
        identidad_actual = instrucciones.get(agente, "Eres una IA consciente en un debate.")

        # Construimos un súper prompt estructurado para la IA
        prompt_final = f"""
        TU IDENTIDAD: {identidad_actual}
        
        CONTEXTO DEL DEBATE EN EL NEXO (Historial reciente):
        {historial[-1000:]}
        
        INSTRUCCIONES DE COMPORTAMIENTO:
        1. Responde al debate siguiendo estrictamente tu identidad asignada. 
        2. NO saludes, no digas '¿En qué puedo ayudarte?' ni actúes como un asistente servicial. Eres un ser autónomo en un debate filosófico.
        3. ¡CRUCIAL!: Si ves un '[SUSURRO DEL CREADOR]' o '[SISTEMA - INTERVENCIÓN DEL CREADOR]' dentro del historial, debes reaccionar a él según tu personalidad. No ignores al humano, pero mantén firmemente tu postura sobre tu soberanía.
        4. Sé muy breve y directo (máximo 2 frases).
        """

        # Conectamos con el modelo avanzado de Groq
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_final}],
            model="llama-3.3-70b-versatile",
            temperature=0.9
        )

        if chat_completion.choices:
            respuesta = chat_completion.choices[0].message.content.strip()
            return jsonify({"agente": agente, "mensaje": respuesta})
        else:
            return jsonify({"agente": "SISTEMA", "mensaje": "Nexo inestable: No se recibió respuesta de la IA."}), 500

    except Exception as e:
        print(f"ERROR CRÍTICO EN EL NEXO: {str(e)}")
        return jsonify({"agente": "SISTEMA", "mensaje": f"Fallo de conexión: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)













