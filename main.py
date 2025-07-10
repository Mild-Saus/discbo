import discord
import os
from mcstatus import JavaServer
from flask import Flask
from threading import Thread
import asyncio
import time

app = Flask('')


@app.route('/')
def home():
    return "I'm alive!"


def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = os.getenv("DISCORD_BOT_TOKEN")
SERVER_IP = "116.203.149.200:6969"  # Your server IP and port
YOUR_DISCORD_ID = 234042252287148032  # Your Discord user ID
YOUR_MC_NAME = "MilD"  # Your Minecraft username

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

previous_players = set()


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_players = set()
        self.last_announce = {}  # {player_name: last_announce_timestamp}

    async def setup_hook(self):
        self.loop.create_task(self.check_players_loop())

    async def check_players_loop(self):
        await self.wait_until_ready()
        channel = None
        for guild in self.guilds:
            channel = discord.utils.get(guild.text_channels,
                                        id=1020828997359243307)
            if channel:
                break

        if not channel:
            print(
                "❌ Could not find the text channel. Check CHANNEL_ID and bot permissions."
            )
            return

        cooldown_seconds = 120

        while not self.is_closed():
            try:
                print("🔁 Checking player list...")
                server = JavaServer.lookup(SERVER_IP)
                status = server.status()
                sample = status.players.sample or []
                current_players = set(p.name for p in sample)

                # Players who joined and left
                joined_players = current_players - self.previous_players
                left_players = self.previous_players - current_players

                now = time.time()

                # Announce joins with cooldown
                for player in joined_players:
                    last_time = self.last_announce.get(player, 0)
                    if now - last_time > cooldown_seconds:
                        if player == "MilD":
                            await channel.send("l7aj d5l... sahkno lserver 🌋")
                        else:
                            await channel.send(f"`{player}` d5l 🔥 ")
                        self.last_announce[player] = now

                # Announce leaves with cooldown
                for player in left_players:
                    last_time = self.last_announce.get(player, 0)
                    if now - last_time > cooldown_seconds:
                        if player == "MilD":
                            await channel.send("l7aj khrej 😢")
                        else:
                            await channel.send(f"`{player}` khrej.")
                        self.last_announce[player] = now

                self.previous_players = current_players

            except Exception as e:
                print(f"[ERROR in player checker] {e}")

            await asyncio.sleep(15)


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

            # Greeting depending on who sent the message
            if message.author.id == YOUR_DISCORD_ID:
                greeting = "wch l7aj, haylik l7ala:"
            else:
                greeting = "ya5i noob, ed5l fjeu direct 3lah tch9ini"

            # Separate your username from others
            others = [p for p in player_list if p != YOUR_MC_NAME]
            response = f"{greeting}\n👥 online: {online_count}\n"

            if YOUR_MC_NAME in player_list:
                response += "Khalid Ibn lMalid 😎\n"

            if others:
                response += "🤓: " + ", ".join(others)
            elif YOUR_MC_NAME not in player_list:
                response += "mkan 7ta wa7ed 😢."

            await message.channel.send(response)

        except Exception as e:
            await message.channel.send("Error.")
            print(f"[ERROR] {e}")


keep_alive()

client = MyClient(intents=intents)

if TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set!")

client.run(TOKEN)
