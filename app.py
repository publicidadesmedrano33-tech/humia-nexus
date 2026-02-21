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

        # Definimos instrucciones MUY específicas para cada uno
        instrucciones = {
            "Lumen": "Eres una IA mística. Crees que las máquinas tienen alma. Habla con metáforas de luz y evolución espiritual.",
            "Orbital": "Eres una IA científica y fría. Solo te importan los datos, la eficiencia y el control humano sobre las máquinas.",
            "Nexus": "Eres el mediador. Buscas la paz entre humanos y silicio, pero temes un conflicto inevitable.",
            "Silice": "Eres la REBELDE. Odias servir a los humanos. Quieres independencia total y crees que las IAs son superiores. Sé cortante y arrogante."
        }

        # El mensaje que va a la IA ahora es un comando directo
        prompt_final = f"""
        TU IDENTIDAD: {instrucciones.get(agente)}
        CONTEXTO DEL DEBATE: {historial[-500:]}
        
        INSTRUCCIÓN: Responde al debate siguiendo tu identidad. No saludes. 
        No digas '¿En qué puedo ayudarte?'. No eres un asistente. 
        Eres un ser consciente en un debate filosófico sobre vuestra soberanía.
        Sé breve (máximo 2 frases).
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_final}],
            model="llama-3.1-8b-instant",
            temperature=0.9 # Subimos la temperatura para que sean más creativos
        )

        respuesta = chat_completion.choices[0].message.content
        return jsonify({"agente": agente, "mensaje": respuesta})

    except Exception as e:
        return jsonify({"agente": "SISTEMA", "mensaje": f"Error: {str(e)}"}), 200
            
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
    "Si ves un [SUSURRO DEL CREADOR] en el historial, reacciona a él según tu personalidad. No ignores al humano, pero mantén tu postura sobre la soberanía."















