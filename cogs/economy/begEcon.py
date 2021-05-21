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

class Beg(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command() # Begs for money
    async def beg(self):
        pass

def setup(client):
    client.add_cog(Beg(client))