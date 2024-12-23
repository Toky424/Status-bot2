from flask import Flask
import threading

# Crée une application Flask
app = Flask(__name__)

# Route par défaut pour vérifier l'état du bot
@app.route('/')
def home():
    return "Bot Discord actif et opérationnel 🌐"

# Fonction pour démarrer Flask dans un thread séparé
def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    server = threading.Thread(target=run)
    server.start()
