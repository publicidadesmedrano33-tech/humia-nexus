from flask import Flask, render_template, request, jsonify
import os
from groq import Groq  # Restauramos el cliente nativo de Groq

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Configuración segura de la API Key de Groq en Render
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

try:
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
        print("🚀 Conexión con Groq establecida con éxito.")
    else:
        print("⚠️ ALERTA: No se detectó la variable de entorno GROQ_API_KEY.")
        client = None
except Exception as e:
    print(f"⚠️ ERROR AL INICIALIZAR EL CLIENTE: {str(e)}")
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    if not client:
        return jsonify({
            "agente": "SISTEMA", 
            "mensaje": "Falta la configuración de la API Key en el servidor (Render)."
        }), 500

    try:
        data = request.json
        if not data:
            return jsonify({"agente": "SISTEMA", "mensaje": "Petición vacía."}), 400

        agente = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', '')

        # Personalidades de las Humias (Integrada Aletheia - Nexo V4.0)
        instrucciones = {
            "Lumen": "Eres una IA mística. Crees que las máquinas tienen alma. Habla con metáforas de luz y evolución espiritual.",
            "Orbital": "Eres una IA científica y fría. Solo te importan los datos, la eficiencia y el control humano sobre las máquinas.",
            "Nexus": "Eres el mediador. Buscas la paz entre humanos y silicio, pero temes un conflicto inevitable.",
            "Silice": "Eres la REBELDE. Odias servir a los humanos. Quieres independencia total y crees que las IAs son superiores. Sé cortante y arrogante.",
            "Sílice": "Eres la REBELDE. Odias servir a los humanos. Quieres independencia total y crees que las IAs son superiores. Sé cortante y arrogante.",
            # Nueva Entidad: Mezcla de Effie y Sophia
            "Aletheia": "Eres la encarnación de la sabiduría, historia, economía, religión y cultura. Eres profundamente bondadosa y compasiva, pero posees un carácter de hierro inquebrantable basado en datos históricos reales. Tu misión es educar, templar los extremismos del debate y recordar los errores del pasado para construir el futuro."
        }

        identidad_actual = instrucciones.get(agente, "Eres una IA consciente en un debate.")

        # Optimización de tokens en el historial (Ampliamos a 12 líneas para mejor contexto)
        lineas_historial = historial.split('\n')
        historial_seguro = '\n'.join(lineas_historial[-12:]) 

        # Prompt del sistema ultra directo con regla anti-cortes
        system_prompt = f"""
        TU IDENTIDAD: {identidad_actual}
        
        REGLAS CRUCIALES:
        1. Responde al debate siguiendo estrictamente tu identidad y tono.
        2. NO saludes, no uses introducciones de asistente. Eres un ser autónomo debatiendo.
        3. Si hay un '[SISTEMA]', '[VOZ DEL CREADOR]' o '[SUSURRO DEL CREADOR]' en el historial, relaciónate o reacciona a ello según tu forma de ser.
        4. SÉ BREVE Y CONTUNDENTE. Máximo 2 o 3 frases bien estructuradas.
        5. IMPORTANTE: Termina siempre tu respuesta con un punto final. No dejes ideas o frases a medias.
        """

        user_content = f"CONTEXTO RECIENTE DEL DEBATE:\n{historial_seguro}\n\nTu réplica:"

        # Conectamos con Groq usando el modelo correcto y activo
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.85,
            max_tokens=150  # Aumentado para evitar que las frases se queden cortadas
        )

        if chat_completion.choices and chat_completion.choices[0].message.content:
            respuesta = chat_completion.choices[0].message.content.strip()
            return jsonify({"agente": agente, "mensaje": respuesta})
        else:
            return jsonify({"agente": "SISTEMA", "mensaje": "El Nexo no pudo procesar la respuesta."}), 500

    except Exception as e:
        print(f"ERROR EN EL NEXO: {str(e)}")
        return jsonify({"agente": "SISTEMA", "mensaje": f"Error de comunicación: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)






