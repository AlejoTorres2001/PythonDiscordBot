import discord
from discord.ext import commands

class Sys(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    def is_admin(self,ctx):
        return ctx.author.id == 470679833844776972
    @commands.command()
    async def clear(self,ctx,amount:int,):
        if(self.is_admin(ctx)):
            await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.send("No tienes permiso de hacer eso")
            

"""Setup"""
def setup(bot):
    bot.add_cog(Sys(bot))