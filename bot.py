import discord
import requests
import asyncio
from dotenv import load_dotenv
import os

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

# Lancer le bot
bot.run(TOKEN)
