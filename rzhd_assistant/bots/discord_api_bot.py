from discord import Client, Intents
from request_to_rasa import get_rasa_answer
from rzhd_assistant.vault import vault_utils

DISCORD_TOKEN = vault_utils.rtrieve_secret('DISCORD_TOKEN')
bot = Client(intents=Intents.default())


@bot.event
async def on_ready():
    print("Everything's all ready to go!")


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        await ctx.reply(get_rasa_answer(ctx.content))

bot.run(DISCORD_TOKEN)
