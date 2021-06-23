import random
from discord.ext import commands
import random

class RandomNumbers(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def random(self,ctx,num1,num2,cant=1):
        try:
            num1=int(num1)
            num2=int(num2)
            for i in range(cant):
                await ctx.send(random.randint(num1,num2))
        except ValueError:
            await ctx.send("Solo Numeros enteros!")











def setup(client):
    client.add_cog(RandomNumbers(client))