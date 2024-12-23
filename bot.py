import discord
import requests
import asyncio
from dotenv import load_dotenv
import os
from flask import Flask

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer le token du bot à partir de la variable d'environnement
TOKEN = os.getenv("DISCORD_TOKEN")

# Intention du bot
intents = discord.Intents.default()

# Crée un client Discord avec un gestionnaire de commandes
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Bot connecté en tant que {self.user} 🌐")
        try:
            # Synchronisation des commandes d'application
            await self.tree.sync()
            print("Commandes synchronisées avec succès. 🌐")
        except Exception as e:
            print(f"Erreur de synchronisation : {e} 🌐")

bot = MyBot()

# Définition de la commande slash
@bot.tree.command(name="status", description="Vérifie le statut d'un site web")
async def status(interaction: discord.Interaction, url: str):
    """Commande slash pour vérifier le statut de n'importe quel site web."""
    # Supprime le message de l'utilisateur
    await interaction.response.defer(thinking=True)

    try:
        # Envoi une requête GET au site fourni
        response = requests.get(url, timeout=5)
        site_name = url.split("//")[-1].split("/")[0]  # Extrait le nom du site

        if response.status_code == 200:
            reply = await interaction.followup.send(
                f"**✅ Le site {site_name} est accessible !** 🌐", 
                ephemeral=False
            )
        else:
            reply = await interaction.followup.send(
                f"**⚠️ Le site {site_name} a répondu avec le code {response.status_code}.** 🌐", 
                ephemeral=False
            )
    except requests.exceptions.RequestException as e:
        reply = await interaction.followup.send(
            f"**❌ Impossible d'accéder au site {url}. Erreur : {e}** 🌐", 
            ephemeral=False
        )
    
    # Supprime la réponse du bot après 30 secondes
    await asyncio.sleep(30)
    await reply.delete()

# Créer un serveur Flask pour être surveillé par UptimeRobot
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Discord en ligne"

# Lancer le bot et le serveur Flask simultanément
if __name__ == '__main__':
    from threading import Thread

    # Fonction pour démarrer le bot
    def run_bot():
        bot.run(TOKEN)

    # Fonction pour démarrer le serveur Flask
    def run_flask():
        app.run(host="0.0.0.0", port=5000)  # Pour Render, l'IP doit être 0.0.0.0

    # Démarrer le bot et le serveur Flask sur des threads différents
    thread_bot = Thread(target=run_bot)
    thread_flask = Thread(target=run_flask)

    thread_bot.start()
    thread_flask.start()
