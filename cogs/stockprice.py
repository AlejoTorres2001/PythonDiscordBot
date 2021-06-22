import discord
from discord.ext import commands
import pandas_datareader as web
import datetime
class StockPrice(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_stock_price(self,ticker):
        data = web.DataReader(ticker, "yahoo")
        return data['Close'].iloc[-1]

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.client.user:  # Evitar que se responda a si mismo
            return
        if message.content.startswith("stockprice"):  # precio de la accion
            try:
                if len(message.content.split(" ")) == 2:
                    ticker = message.content.split(" ")[1]
                    price = self.get_stock_price(ticker)
                    await message.channel.send(f"stock proce of {ticker} is {price}")

            except(Exception):
                await message.channel.send(f"Nose que concha es {ticker} ")


def setup(client):
    client.add_cog(StockPrice(client))