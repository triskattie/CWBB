import discord
from discord.ext import commands
import json
import os

from dotenv import load_dotenv

load_dotenv()
token = os.environ['BOT_TOKEN']

source_channel_id = 1419435979374334035
dest_channel_id = 1419435776869007361
role_mention_id = 1414130283099193444

intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load previous message IDs
cached_path = os.path.join(os.path.dirname(__file__), "cached.json")
if os.path.exists(cached_path):
    with open(cached_path, "r") as f:
        cached = set(json.load(f))
else:
    cached = set()

def save_cached(cached):
    with open("cached.json", "w") as f:
        json.dump(list(cached), f)

@bot.event
async def on_ready():
    print("Bot is ready.")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != source_channel_id:
        return

    if str(payload.emoji) != "✅":
        return

    if payload.message_id in cached:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    dest_channel = bot.get_channel(dest_channel_id)
    await dest_channel.send(f"<@&{role_mention_id}>\n{message.content}")

    cached.add(payload.message.id)
    save_cached(cached)

bot.run(token)