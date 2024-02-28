import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from request_to_rasa import get_rasa_json

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Client(intents=discord.Intents.default())


@bot.event
async def on_ready():
    print("Everything's all ready to go!")


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        await ctx.reply(get_rasa_json(ctx.content))

bot.run(DISCORD_TOKEN)
