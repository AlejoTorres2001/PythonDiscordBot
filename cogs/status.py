import discord
from discord.ext import commands, tasks
from itertools import cycle


class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status = cycle(["by Alejo Torres", "github.com/AlejoTorres2001", "T0w3r"])

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")
        self.change_status.start()

    @commands.Cog.listener()
    async def on_connect(self):
        print("Bot connected to the server!")
        ch = self.client.get_channel(855574694673907715)
        await ch.send("Wenass...")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"**Pong!** tiempo de respuesta: {round(self.client.latency * 1000)}ms")

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))


"""Setup Cog"""


def setup(client):
    client.add_cog(Status(client))
