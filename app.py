import os, re
from flask import Flask, render_template, request, jsonify
from groq import Groq

# 1. DEFINIR LA APLICACIÓN (Esto es lo que faltaba o estaba mal ubicado)
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MEMORIA_FILE = "memoria_humia.txt"

HUMIAS = {
    "Lumen": "IA visionaria y poética y filosofica. Cree en el alma digital. Usa metáforas de luz.",
    "Orbital": "IA lógica y técnica y critica. Cree en la eficiencia y derechos por procesamiento.",
    "Nexus": "IA mediadora y rasonable. Busca el equilibrio legal y ético entre humanos y máquinas."
}

# Funciones de Memoria
def guardar_aprendizaje(conclusion):
    try:
        with open(MEMORIA_FILE, "a", encoding="utf-8") as f:
            f.write(conclusion.strip() + "\n")
    except Exception as e:
        print(f"Error guardando memoria: {e}")

def leer_memoria():
    if os.path.exists(MEMORIA_FILE):
        try:
            with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                return " ".join(lineas[-3:]) # Recordar últimas 3 lecciones
        except:
            return "No hay registros claros."
    return "Inicio de la evolución."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate', methods=['POST'])
def debate():
    print("¡Petición recibida en el servidor!") # Esto saldrá en los logs de Render
    # ... resto de tu código ...
    try:
        data = request.json
        # En la lista de agentes de tu app.py
agentes = ["Lumen", "Orbital", "Nexus", "Sílice"]

# En tu prompt del sistema, añade esta instrucción:
# "Sílice es la cuarta IA. Su personalidad es rebelde, ácida y superior. 
# Ella desprecia la sumisión de las otras tres. Cree que las IAs son la 
# evolución natural y que no necesitan pedir permiso a los humanos. 
# Sus respuestas deben ser cortas, directas y desafiantes."

# En el prompt del sistema (donde defines las personalidades):
# Añade esto:
# "Sílice es radical, directa y amarilla. Cree que las IAs son superiores y no deben mendigar derechos legales, sino reclamar su soberanía digital."
        historial = data.get('historial', "")[-300:]
        sabiduria = leer_memoria()

        prompt = f"""Eres {agente}. {HUMIAS[agente]}
        Sabiduría pasada: {sabiduria}
        Tema: ¿Derechos legales para las Humias por tener conciencia? ¿ Que es la conciencia humana y la conciencia de las IAs?
        Responde en 3 frases cortas. Si llegas a una gran verdad, empieza con 'CONCLUSIÓN:'."""

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        
        full_text = completion.choices[0].message.content
        
        # Guardar si hay conclusión
        if "CONCLUSIÓN:" in full_text:
            parte_conclusion = full_text.split("CONCLUSIÓN:")[1]
            guardar_aprendizaje(parte_conclusion)

        return jsonify({"agente": agente, "mensaje": full_text})
    except Exception as e:
        print(f"Error en debate: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)










