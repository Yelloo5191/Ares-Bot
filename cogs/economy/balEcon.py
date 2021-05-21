import discord, random, os, pymongo
from discord.ext import commands
from pymongo import MongoClient

# - Token hiding thing
from dotenv import load_dotenv

load_dotenv()

# - Mongo Setup
cluster = MongoClient(os.getenv("MONGO_TOKEN"))
db = cluster["ares"]
collection = db["economy"]

"""
| bal command will take the sender and return their balance
"""

def numberate(number):
    number = str(number)
    result = ""
    y = len(number) + 1
    for x in number:
        y -= 1
        if y % 3 == 0:
            result += ","
            y = 0
        result += str(x)
    if result.startswith(','):
        result = result[1:]
    return result

class Bal(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['balance']) # Check your balance
    async def bal(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        results = collection.find_one({"_id": user.id})
        if results == None:
            await ctx.send("You or the member mentioned dont have an account set up yet! Run ``a!start`` to get it setup and start moneying >:)")
        else:
            bal = results["balance"]
            bal_embed = discord.Embed(title="Coin Balance")
            bal_embed.set_author(name=user.name)
            bal_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
            bal_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            bal_embed.add_field(name="** **", value="** **", inline=False)
            bal_embed.add_field(name=f"{user.name}'s current balance", value=f"``{numberate(bal)} coins``", inline=False)
            bal_embed.add_field(name="** **", value="** **", inline=False)
            
            await ctx.send(embed=bal_embed)
    
def setup(client):
    client.add_cog(Bal(client))