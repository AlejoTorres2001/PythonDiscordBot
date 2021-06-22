import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
from cogs.prefix import get_prefix

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}:{[command.name for command in mapping[cog]]}')
    async def send_cog_help(self, cog):
        return await self.get_destination().send(f'{cog.qualified_name}:{[command.name for command in cog.get_commands()]}')
    async def send_group_help(self, group):
        return await self.get_destination().send(f'{group.name}:{[command.name for index,command in enumerate(group.commands)]}')
    async def send_command_help(self, command):
        return await self.get_destination().send(command.name)


client = commands.Bot(command_prefix = get_prefix,help_command=CustomHelpCommand())


@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        print(error)
        await  ctx.send("No entiendo... busca tu comando con !help")

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')
@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
@client.command()
async def reload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
load_dotenv()
TOKEN=os.getenv('TOKEN')
client.run(TOKEN)