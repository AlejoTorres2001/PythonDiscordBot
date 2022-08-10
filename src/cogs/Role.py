import discord
from discord.ext import commands

class Role(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload):
    guild = self.bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name="Hacker")
    await payload.member.add_roles(role, reason="you are a Hacker", atomic=True)
    
def setup(bot):
  bot.add_cog(Role(bot))