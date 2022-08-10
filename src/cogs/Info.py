import discord
from discord.ext import commands

class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def getchannel(self,ctx):
    channels_names = [c.name for c in ctx.guild.channels if type(c) is discord.TextChannel]
    print(channels_names)


def setup(bot):
  bot.add_cog(Info(bot))