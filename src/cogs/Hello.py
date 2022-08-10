import discord
from discord.ext import commands

class Hello(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
    
    @commands.command()
    async def hello(self,ctx):
      user=ctx.message.author.name
      embed=discord.Embed(title="Hello",description=f"Hello {user}",color=0x00ff00)
      await ctx.send(embed=embed)
      
    @commands.command()
    async def dmme(self,ctx):
      user = ctx.message.author.name
      await ctx.author.send(f"Hello {user}")
      
def setup(bot):
    bot.add_cog(Hello(bot))