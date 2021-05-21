import discord, random, os, pymongo
from discord.ext import commands
from pymongo import MongoClient
import datetime

# - Token hiding thing
from dotenv import load_dotenv

load_dotenv()

# - Mongo Setup
cluster = MongoClient(os.getenv("MONGO_TOKEN"))
db = cluster["ares"]
collection = db["economy"]

"""
| start command will intiate the sender into the mongodb economy database and allow them to use the economy features 
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


class Start(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command() # Initiate Economy Account
    async def start(self, ctx):
        results = collection.find_one({"_id":ctx.author.id})
        if results != None:
            balance = results["balance"]
            await ctx.send(f"Your account is already set up! Your balance is ``{numberate(balance)} coins``.")
        else:
            post = {"_id": ctx.author.id, "name": ctx.author.name, "balance": 50, "rewards": True, "dateTimeR": datetime.datetime(2017, 6, 21, 18, 25, 30)}
            collection.insert_one(post)
            results = collection.find_one({"_id":ctx.author.id})
            balance = results["balance"]
            await ctx.send(f"Congrats {ctx.author.name}! Your account has been setup and your starting balance is currently at ``{numberate(balance)} coins``!")
    
def setup(client):
    client.add_cog(Start(client))