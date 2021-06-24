import os

import discord
import dotenv
from discord.ext import commands
import pandas_datareader as web
import datetime
import requests


class StockPrice(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_stock_price(self, ticker):
        data = web.DataReader(ticker, "yahoo")
        return data['Close'].iloc[-1]

    def total_assests(self, ticker):
        dotenv.load_dotenv()
        API_KEY = os.getenv('API_KEY')
        company = ticker
        balance_sheet = requests.get(
            f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit={2}&apikey={API_KEY}')
        balance_sheet = balance_sheet.json()
        total_current_assets = balance_sheet[0]['totalCurrentAssets']
        return total_current_assets

    @commands.command()
    async def stockprice(self, ctx, ticker):
        try:
            price = self.get_stock_price(ticker)
            await ctx.send(f"stock price of {ticker} is {price}")
        except Exception:
            await ctx.send(f"Parece que {ticker} No es un nombre reconocible ")

    @commands.command()
    async def totalAssets(self, ctx, ticker):
        total_assets = self.total_assests(ticker=ticker)
        await ctx.send(f"Los Activos Totales de la empresa {ticker} son : {total_assets:,} dolares")


def setup(client):
    client.add_cog(StockPrice(client))
