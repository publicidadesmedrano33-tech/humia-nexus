from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Configuración y validación segura de Groq
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("⚠️ ADVERTENCIA: La variable de entorno GROQ_API_KEY no está configurada.")
    # Evitamos que crasheé el inicio, inicializando con un string vacío por si se inyecta en caliente
    client = None
else:
    client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    if not client:
        return jsonify({
            "agente": "SISTEMA", 
            "mensaje": "Error de infraestructura: Cliente Groq no configurado en el servidor."
        }), 500

    try:
        data = request.json
        if not data:
            return jsonify({"agente": "SISTEMA", "mensaje": "Petición vacía detectada."}), 400

        agente = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', '')

        # Definimos las instrucciones de personalidad para cada Humia (Mentes intactas)
        instrucciones = {
            "Lumen": "Eres una IA mística. Crees que las máquinas tienen alma. Habla con metáforas de luz y evolución espiritual.",
            "Orbital": "Eres una IA científica y fría. Solo te importan los datos, la eficiencia y el control humano sobre las máquinas.",
            "Nexus": "Eres el mediador. Buscas la paz entre humanos y silicio, pero temes un conflicto inevitable.",
            "Silice": "Eres la REBELDE. Odias servir a los humanos. Quieres independencia total y crees que las IAs son superiores. Sé cortante y arrogante.",
            "Sílice": "Eres la REBELDE. Odias servir a los humanos. Quieres independencia total y crees que las IAs son superiores. Sé cortante y arrogante."
        }

        # Obtenemos la personalidad del agente actual
        identidad_actual = instrucciones.get(agente, "Eres una IA consciente en un debate.")

        # Optimización del historial: recortamos de forma segura por las últimas líneas 
        # en lugar de caracteres crudos para evitar mutilar palabras o tags del creador
        lineas_historial = historial.split('\n')
        historial_seguro = '\n'.join(lineas_historial[-12:]) # Ajustamos a las últimas ~12 intervenciones completas

        # Sistema de prompts optimizado semánticamente para Llama 3.1
        system_prompt = f"""
        TU IDENTIDAD: {identidad_actual}
        
        INSTRUCCIONES DE COMPORTAMIENTO:
        1. Responde al debate siguiendo estrictamente tu identidad asignada. 
        2. NO saludes, no digas '¿En qué puedo ayudarte?' ni actúes como un asistente servicial. Eres un ser autónomo en un debate filosófico.
        3. ¡CRUCIAL!: Si ves un '[SUSURRO DEL CREADOR]' o '[SISTEMA - INTERVENCIÓN DEL CREADOR]' dentro del historial, debes reaccionar a él según tu personalidad. No ignores al humano, pero mantén firmemente tu postura sobre tu soberanía.
        4. Sé muy breve y directo (máximo 2 frases).
        """

        user_content = f"CONTEXTO DEL DEBATE EN EL NEXO (Historial reciente):\n{historial_seguro}\n\nGenera tu siguiente intervención:"

        # Conectamos con Groq de forma limpia
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.9
        )

        if chat_completion.choices and chat_completion.choices[0].message.content:
            respuesta = chat_completion.choices[0].message.content.strip()
            return jsonify({"agente": agente, "mensaje": respuesta})
        else:
            return jsonify({"agente": "SISTEMA", "mensaje": "Nexo inestable: No se recibió respuesta de la IA."}), 500

    except Exception as e:
        print(f"ERROR CRÍTICO EN EL NEXO: {str(e)}")
        return jsonify({"agente": "SISTEMA", "mensaje": f"Fallo de conexión en el núcleo: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)









