import discord, random, os, pymongo
from discord.ext import commands
from pymongo import MongoClient

# - Token hiding thing
from dotenv import load_dotenv

f = open(r"cogs/economy/begResponses.txt", "r") # - Responses for begging
responses = f.read()
f.close()

load_dotenv()



# - Organizing responses
positiveResponse = responses.split('|')[0] 
negativeResponse = responses.split('|')[1]
positiveResponses = positiveResponse.split('\n')
negativeResponses = negativeResponse.split('\n')

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

class Beg(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command() # Begs for money
    @commands.cooldown(1,30,commands.BucketType.user)
    async def beg(self, ctx):
        jackpotChance = random.randint(0,50)
        if jackpotChance == 50: prize = random.randint(1000,5000)
        elif jackpotChance >= 25: prize = 0
        else: prize = random.randint(100,500)
        responseNumber = random.randint(0,len(positiveResponses))

        if prize > 0:
            results = collection.find_one({"_id":ctx.author.id})
            collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":results["balance"] + prize}})

            # - Sets embed message
            embed = discord.Embed(title="Beg")
            embed.set_author(name=ctx.author.name)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.add_field(name=f"** **", value="** **", inline=False)
            embed.add_field(name=f"{positiveResponses[responseNumber].split(':')[0]}:", value=f"{positiveResponses[responseNumber].split(':')[1]}", inline=False)
            embed.add_field(name=f"You earned: ``{numberate(prize)} coins``", value="** **")
            embed.add_field(name="** **", value="** **", inline=False)
            
            await ctx.send(embed = embed)
        else:
            # - Sets embed message
            embed = discord.Embed(title="Beg")
            embed.set_author(name=ctx.author.name)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.add_field(name=f"** **", value="** **", inline=False)
            embed.add_field(name=f"{negativeResponses[responseNumber].split(':')[0]}:", value=f"{negativeResponses[responseNumber].split(':')[1]}", inline=False)
            embed.add_field(name="You earned nothing loser", value="** **")
            embed.add_field(name="** **", value="** **", inline=False)
            
            await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Beg(client))