from discord.ext import commands
import os
from dotenv import load_dotenv,find_dotenv

def load_all_cogs(bot):
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

load_dotenv(find_dotenv())
bot = commands.Bot(command_prefix='!')

load_all_cogs(bot)

bot.run(os.getenv('DISCORD_API_TOKEN'))
