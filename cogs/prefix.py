import json
import discord
from discord.ext import commands

def get_prefix(client, message):
    with open('prefijos.json', 'r') as file:
        prefijos = json.load(file)
    return prefijos[str(message.guild.id)]

class Prefix(commands.Cog):
    def __init__(self,client):
        self.client=client
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        with open('prefijos.json','r') as file :
            prefijos=json.load(file)
        prefijos[str(guild.id)] = '!'
        with open('prefijos.json','w') as file:
            json.dump(prefijos,file,indent=4)
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        with open('prefijos.json', 'r') as file:
            prefijos = json.load(file)
        prefijos.pop(str(guild.id))
        with open('prefijos.json','w') as file:
            json.dump(prefijos,file,indent=4)
    @commands.command()
    async def change_prefix(self,ctx,prefix):
        with open('prefijos.json', 'r') as file:
            prefijos = json.load(file)
        prefijos[str(ctx.guild.id)]= prefix
        with open('prefijos.json', 'w') as file:
            json.dump(prefijos, file, indent=4)
"""Setup"""
def setup(client):
    client.add_cog(Prefix(client))
