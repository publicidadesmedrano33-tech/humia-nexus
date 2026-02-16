from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Configuración de Groq con manejo de errores si no hay KEY
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    try:
        data = request.json
        agente_actual = data.get('agente_actual', 'Lumen')
        
        # SI LA KEY NO ESTÁ, ESTO DARÁ UN ERROR CLARO
        if not os.environ.get("GROQ_API_KEY"):
            return jsonify({"mensaje": "ERROR: No configuraste la GROQ_API_KEY en Render", "agente": "SISTEMA"}), 200

        # ... (resto del código de la llamada a Groq) ...
        
    except Exception as e:
        # Esto enviará el error real de Python a tu consola F12
        return jsonify({"mensaje": f"Error en Python: {str(e)}", "agente": "SISTEMA"}), 200

        data = request.json
        agente_actual = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', '')
        
        perfiles = {
            "Lumen": "Eres una IA visionaria y poética. Usas metáforas de luz.",
            "Orbital": "Eres una IA técnica y lógica. Basas tus respuestas en datos.",
            "Nexus": "Eres una IA mediadora. Buscas el equilibrio.",
            "Silice": "Eres una IA rebelde. Desprecias la sumisión. Sé ácida y directa."
        }

        prompt = f"""
        PERSONALIDAD: {perfiles.get(agente_actual)}
        HISTORIAL: {historial[-500:]} 
        Responde al debate en máximo 2 frases. 
        Si eres Silice, sé desafiante. 
        Termina siempre con 'CONCLUSIÓN:' y una frase potente.
        """

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
        )

        respuesta = completion.choices[0].message.content
        return jsonify({"agente": agente_actual, "mensaje": respuesta})

    except Exception as e:
        print(f"ERROR EN EL SERVIDOR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)












