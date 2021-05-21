import discord, random, os, pymongo
from discord.ext import commands
from pymongo import MongoClient

# - Token hiding thing
from dotenv import load_dotenv

load_dotenv()

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

# - Mongo Setup
cluster = MongoClient(os.getenv("MONGO_TOKEN"))
db = cluster["ares"]
collection = db["economy"]

class Leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["top", "rank"]) # - Displays Global Leaderboard
    async def leaderboard(self, ctx):
        results = collection.find({})
        namesAndBalance = {}
        for x in results:
            namesAndBalance[x["name"]] = x["balance"]
        sortedDict = dict(sorted(namesAndBalance.items(), key=lambda item: item[1], reverse=True))
        nameList = []
        balanceList = []
        
        for x in sortedDict:
            nameList.append(x)
        for y in nameList:
            balanceList.append(sortedDict[y])

        lead = discord.Embed(title="Global Leaderboard", description="Top balance: ")
        lead.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")

        for x in range(10):
            try:
                lead.add_field(name= str(x + 1) + ") " + nameList[x], value= "`" + numberate(balanceList[x]) + " coins`", inline = False)
            except IndexError:
                lead.add_field(name= str(x + 1) + ") " + "N/a", value= "** **", inline = False)

        lead.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

        await ctx.send(embed = lead)
    
def setup(client):
    client.add_cog(Leaderboard(client))