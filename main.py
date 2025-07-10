import discord
import os
from mcstatus import JavaServer

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
SERVER_IP = "116.203.149.200:6969"  # Your server IP and port
YOUR_DISCORD_ID = 234042252287148032  # Your Discord user ID
YOUR_MC_NAME = "MilD"  # Your Minecraft username

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"✅ Bot connected as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!players"):
        try:
            server = JavaServer.lookup(SERVER_IP)
            status = server.status()

            # Get list of player names (if available)
            player_sample = status.players.sample or []
            player_list = [p.name for p in player_sample]
            online_count = status.players.online
            max_players = status.players.max

            # Greeting depending on who sent the message
            if message.author.id == YOUR_DISCORD_ID:
                greeting = "wch l7aj, haylik l7ala:"
            else:
                greeting = "ya5i noob, ed5l fjeu direct 3lah tch9ini"

            # Separate your username from others
            others = [p for p in player_list if p != YOUR_MC_NAME]
            response = f"{greeting}\n👥 online: {online_count}\n"

            if YOUR_MC_NAME in player_list:
                response += f"Khalid Ibn lMalid 😎\n"

            if others:
                response += "🤓: " + ", ".join(others)
            elif YOUR_MC_NAME not in player_list:
                response += "mkan 7ta wa7ed 😢."

            await message.channel.send(response)

        except Exception as e:
            await message.channel.send("Error.")
            print(f"[ERROR] {e}")


client.run(TOKEN)
