import discord
from discord.ext import commands


class Sys(commands.Cog):
    def __init__(self,client):
        self.client=client

    def soyYo(self,ctx):
        return ctx.author.id == 470679833844776972
    @commands.command()
    async def clear(self,ctx, amount:int,):
        if(self.soyYo(ctx)):
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send("No tienes permiso de hacer eso")

    @commands.command()
    async def sys_k(self,ctx, member: discord.Member, *, reason=None):
        if(self.soyYo(ctx)):
            await member.kick(reason=reason)
        else:
            await ctx.send("No tienes permiso de hacer eso")

    @commands.command()
    async def sys_b(self,ctx, member: discord.Member, *, reason=None):
        if(self.soyYo(ctx)):
            await member.ban(reason=reason)
            await ctx.send(f"baneo a {member.mention}")
        else:
            await ctx.send("No tienes permiso de hacer eso")


    @commands.command()
    async def sys_unb(self,ctx, member):
        if(self.soyYo(ctx)):
            banned_users = await ctx.guild.bans()
            name, disc = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (name, disc):
                    await ctx.guild.unban(user)
                    await  ctx.send(f"des-baneo a {user.mention}")
                    return
        else:
            await ctx.send("No tienes permiso de hacer eso")

    @commands.command()
    async def on_member_join(self,ctx,member):
        await ctx.send(f"Bienvenido{member}!")
        print(f"{member} has joined the server")

    """Error Handling"""
    @clear.error
    async def clear_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("cuantos mensajes borro? (!clear int)")
            print("Error!")




"""Setup"""
def setup(client):
    client.add_cog(Sys(client))

