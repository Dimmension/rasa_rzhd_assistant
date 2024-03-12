import os
from discord import Client, Intents
from dotenv import load_dotenv
from request_to_rasa import get_rasa_answer

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = Client(intents=Intents.default())


@bot.event
async def on_ready():
    print("Everything's all ready to go!")


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        await ctx.reply(get_rasa_answer(ctx.content))

bot.run(DISCORD_TOKEN)
