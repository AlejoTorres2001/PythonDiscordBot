import discord
from discord.ext import commands,tasks
from itertools import  cycle

class Status(commands.Cog):

    def __init__(self,client):
        self.client=client
        self.status=cycle(["by Alejo Torres","T0w3r"])
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")
        self.change_status.start()
    @commands.command()
    async def ping(self,ctx):
        await ctx.send("Pong!")
    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))



def setup(client):
    client.add_cog(Status(client))