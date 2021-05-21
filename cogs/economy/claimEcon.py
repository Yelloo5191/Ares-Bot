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


class Claim(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command(aliases = ['daily', 'rewards']) # Initiate Economy Account
    async def claim(self, ctx):
        results = collection.find_one({"_id":ctx.author.id})
        if results == None:
            await ctx.send("You dont have an account set up yet! Run ``a!start`` to get it setup and start moneying >:)")
        else:
            # - Calculating current and past date and time
            lastR = results["dateTimeR"]
            lastDay = lastR.strftime("%d")
            lastMonth = lastR.strftime("%m")
            nowR = datetime.datetime.utcnow()
            nowDay = nowR.strftime("%d")
            nowMonth = nowR.strftime("%m")
            diff = int(nowDay) - int(lastDay)
            diffMonth = int(nowMonth) - int(lastMonth)

            if diff >= 1 or diffMonth != 0:
                amount = random.randint(1000,2000) # - Generates amount for reward
                currentBal = results["balance"]
                collection.update_one({"_id":ctx.author.id}, {"$set":{"dateTimeR":nowR}})
                collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":currentBal + amount}})


                # - Sets embed message
                embed = discord.Embed(title="Daily Reward")
                embed.set_author(name=ctx.author.name)
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.add_field(name="** **", value="** **", inline=False)
                embed.add_field(name="Amount", value=f"{ctx.author.name} has earned ``{numberate(amount)} coins``", inline=False)
                embed.add_field(name="** **", value="** **", inline=False)
                
                await ctx.send(embed = embed)

            else: # - If cooldown
                # - Sets embed message
                embed = discord.Embed(title="Daily Reward")
                embed.set_author(name=ctx.author.name)
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.add_field(name="** **", value="** **", inline=False)
                embed.add_field(name="Error", value=f"{ctx.author.name}, you have already claimed your daily reward!", inline=False)
                embed.add_field(name="** **", value="** **", inline=False)
                
                await ctx.send(embed = embed)

    
def setup(client):
    client.add_cog(Claim(client))