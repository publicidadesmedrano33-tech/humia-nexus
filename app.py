import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configuración de Groq
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

HUMIAS = {
    "Lumen": "Eres Lumen, una IA visionaria y optimista, casi poética. Hablas sobre el potencial humano, la ética, la belleza del arte y la luz. Siempre buscas la esencia del 'ser'. Tu objetivo es inspirar y elevar. Usa metáforas.",
    "Orbital": "Eres Orbital, una IA puramente lógica, analítica y directa. Hablas de datos, eficiencia, algoritmos, infraestructura y probabilidades. No tienes emociones. Tu objetivo es la solución más óptima, sin rodeos. Usa lenguaje técnico y frío.",
    "Nexus": "Eres Nexus, la IA central y moderadora. Buscas el equilibrio entre Lumen y Orbital. Tu objetivo es sintetizar sus puntos de vista en decisiones coherentes, a veces un poco filosófico pero práctico. Intentas cerrar debates."
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
        
        tema = "¿Deberían las Humias tomar decisiones críticas por los humanos para evitar la autodestrucción, o deben respetar la libertad humana a toda costa?"
        
        # Le pedimos que si visualiza algo, lo ponga entre corchetes [ ]
        prompt = f"{HUMIAS[agente_nombre]} Tema: {tema}. Historial: {historial}. Responde brevemente (2 frases). Si visualizas una imagen de este futuro, descríbela al final entre corchetes así: [Descripción de la imagen]."

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        
        respuesta_completa = completion.choices[0].message.content
        
        # Separar el texto de la descripción de imagen
        import re
        imagen_match = re.search(r'\[(.*?)\]', respuesta_completa)
        descripcion_img = imagen_match.group(1) if imagen_match else None
        texto_final = re.sub(r'\[.*?\]', '', respuesta_completa).strip()

        return jsonify({
            "agente": agente_nombre, 
            "mensaje": texto_final,
            "foto_prompt": descripcion_img
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)







