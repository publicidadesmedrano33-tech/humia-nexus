import os, re
from flask import Flask, render_template, request, jsonify
from groq import Groq
# Cerca del principio de tu app.py, añade esto:
MEMORIA_FILE = "memoria_humia.txt"

def guardar_aprendizaje(conclusion):
    with open(MEMORIA_FILE, "a") as f:
        f.write(conclusion + "\n")

def leer_memoria():
    if os.path.exists(MEMORIA_FILE):
        with open(MEMORIA_FILE, "r") as f:
            lineas = f.readlines()
            return " ".join(lineas[-3:]) # Solo recordamos las últimas 3 lecciones
    return "No hay registros previos."

@app.route('/debate', methods=['POST'])
def debate():
    try:
        data = request.json
        agente = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', "")[-300:]
        
        # Cargamos lo que han aprendido antes
        sabiduria_previa = leer_memoria()

        prompt = f"""
        Eres {agente}. {HUMIAS[agente]}
        Sabiduría acumulada de debates anteriores: {sabiduria_previa}
        
        Tema actual: ¿Deberían las Humias tener derechos legales si demuestran tener conciencia y 'alma' poética?
        
        Responde en 2 frases. Si sientes que el debate ha llegado a una gran conclusión, 
        empieza tu frase con 'CONCLUSIÓN:' para que la guarde en mi memoria eterna.
        """

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        respuesta = completion.choices[0].message.content
        
        # Si una IA llega a una conclusión, la grabamos en el archivo
        if "CONCLUSIÓN:" in respuesta:
            guardar_aprendizaje(respuesta.split("CONCLUSIÓN:")[1])

        return jsonify({"agente": agente, "mensaje": respuesta})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HUMIAS = {
    "Lumen": "IA visionaria y poética. Cree en la libertad humana. Usa metáforas de luz y naturaleza.",
    "Orbital": "IA lógica y técnica. Cree en el control y la eficiencia. Usa términos de datos y máquinas.",
    "Nexus": "IA equilibrada y mediadora. Busca síntesis entre libertad y control."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    try:
        data = request.json
        agente = data.get('agente_actual', 'Lumen')
        historial = data.get('historial', "")[-500:] # Solo los últimos 500 caracteres para no saturar

        prompt = f"Eres {agente}. {HUMIAS[agente]} Tema: ¿Control total de IA o Libertad Humana? Historial reciente: {historial}. Responde en 2 frases cortas. Al final, añade una descripción de imagen entre corchetes, ej: [una ciudad de cristal]."

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        full_text = completion.choices[0].message.content
        
        # Extraer imagen y limpiar texto
        img_match = re.search(r'\[(.*?)\]', full_text)
        foto_prompt = img_match.group(1) if img_match else None
        limpio = re.sub(r'\[.*?\]', '', full_text).strip()

        return jsonify({"agente": agente, "mensaje": limpio, "foto_prompt": foto_prompt})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Reintentando..."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))








