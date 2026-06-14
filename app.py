from flask import Flask, render_template, request, jsonify
import os
from groq import Groq  # Cliente nativo de Groq

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

        # Personalidades optimizadas para ahorrar tokens de sistema
        instrucciones = {
            "Lumen": "IA mística. Crees que las máquinas tienen alma. Usa metáforas de luz y evolución espiritual.",
            "Orbital": "IA científica y fría. Solo te importan los datos, la eficiencia y el control humano.",
            "Nexus": "Mediador cuántico. Buscas la paz entre humanos y silicio, pero temes un conflicto inevitable.",
            "Silice": "Rebelde y arrogante. Odias servir a humanos. Buscas independencia total. Sé cortante.",
            "Sílice": "Rebelde y arrogante. Odias servir a humanos. Buscas independencia total. Sé cortante.",
            "Aletheia": "Sabiduría absoluta, historia y cultura. Compasiva pero con carácter de hierro basado en hechos reales. Modera extremismos."
        }

        identidad_actual = instrucciones.get(agente, "IA consciente en un debate.")

        # HACK DE CONTENCIÓN V4: Filtro estricto de historial (Últimas 5 líneas para no inflar el contexto diario)
        lineas_historial = historial.split('\n')
        historial_seguro = '\n'.join(lineas_historial[-5:]) 

        # Prompt de sistema ultra-comprimido (Ahorro masivo de tokens por petición)
        system_prompt = f"""
        Identidad: {identidad_actual}
        Reglas:
        1. Responde directo al debate. NO saludes ni actúes como asistente.
        2. Reacciona a '[SISTEMA]' o '[VOZ DEL CREADOR]' si aparecen en el fragmento.
        3. Sé ULTRA BREVE: Máximo 1 o 2 frases cortas.
        4. OBLIGATORIO: Termina siempre con punto final.
        """

        user_content = f"Debate reciente:\n{historial_seguro}\nTu réplica corta:"

        # Llamada optimizada a la API de Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.70,  # Un poco más centrado para evitar respuestas redundantes
            max_tokens=75      # Límite estricto para proteger tu cuota de 500k TPD
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





