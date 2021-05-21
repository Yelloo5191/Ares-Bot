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
| pay command will take the specified amount from the sender and send it over to the receiver
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

class Pay(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["give"]) # Pay money to a friend
    async def pay(self, ctx, user: discord.Member, amount: int):
        results = collection.find_one({"_id":ctx.author.id})
        if results == None:
            await ctx.send("You dont have an account set up yet! Run ``a!start`` to get it setup and start moneying >:)")
        else:
            sender = collection.find_one({"_id":ctx.author.id})
            receiver = collection.find_one({"_id": user.id})
            if sender["balance"] - amount < 0:
                await ctx.send("You can't afford that silly!")
            else:
                balsender = sender["balance"]
                balreceiver = receiver["balance"]
                collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":balsender-amount}})
                collection.update_one({"_id":user.id}, {"$set":{"balance":balreceiver+amount}})

                pay_embed = discord.Embed(title="Payment")
                pay_embed.set_author(name=user.name)
                pay_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                pay_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                pay_embed.add_field(name="** **", value="** **", inline=False)
                pay_embed.add_field(name="Amount", value=f"{ctx.author.name} has payed {user.name} ``{numberate(amount)} coins``", inline=False)
                pay_embed.add_field(name="** **", value="** **", inline=False)

                await ctx.send(embed=pay_embed)
    
def setup(client):
    client.add_cog(Pay(client))