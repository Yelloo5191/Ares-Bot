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

class Bet(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['gamble']) # Gambling
    @commands.cooldown(1,10,commands.BucketType.user)
    async def bet(self, ctx, amount=10):
        amount = int(amount)
        results = collection.find_one({"_id": ctx.author.id})
        if results == None:
            await ctx.send("You dont have an account set up yet! Run ``a!start`` to get it setup and start moneying >:)")
        else:
            if amount > results["balance"]:
                balresult = results["balance"]

                bet_embed = discord.Embed(title="Gamble")
                bet_embed.set_author(name=ctx.author.name)
                bet_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                bet_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                bet_embed.add_field(name="** **", value="** **", inline=False)
                bet_embed.add_field(name=f"Error", value=f"You can't afford to bet that much, your current balance is ``{numberate(balresult)} coins``", inline=False)
                bet_embed.add_field(name="** **", value="** **", inline=False)

                await ctx.send(embed=bet_embed)
            else:
                collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":results["balance"]-amount}})
                chances = random.randint(0,101)
                if chances <= 39: # Doubled money
                    collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":results["balance"]+amount*2}})
                    results = collection.find_one({"_id": ctx.author.id})
                    balresult = results["balance"]

                    bet_embed = discord.Embed(title="Gamble")
                    bet_embed.set_author(name=ctx.author.name)
                    bet_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                    bet_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    bet_embed.add_field(name="** **", value="** **", inline=False)
                    bet_embed.add_field(name=f"Congrats! You doubled your money!", value=f"You earned ``{numberate(amount*2)} coins`` leaving you with a balance of ``{numberate(balresult)} coins``", inline=False)
                    bet_embed.add_field(name="** **", value="** **", inline=False)

                    await ctx.send(embed=bet_embed)

                elif chances > 39 and chances <= 99:
                    results = collection.find_one({"_id": ctx.author.id})
                    balresult = results["balance"]

                    bet_embed = discord.Embed(title="Gamble")
                    bet_embed.set_author(name=ctx.author.name)
                    bet_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                    bet_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    bet_embed.add_field(name="** **", value="** **", inline=False)
                    bet_embed.add_field(name=f"Sorry, you lost :D!", value=f"Your balance is now ``{numberate(balresult)} coins``", inline=False)
                    bet_embed.add_field(name="** **", value="** **", inline=False)

                    await ctx.send(embed=bet_embed)

                elif chances == 100:
                    jackpotAmount = random.randint(amount*5, amount*10)
                    collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":results["balance"]+jackpotAmount}})
                    results = collection.find_one({"_id": ctx.author.id})
                    balresult = results["balance"]

                    bet_embed = discord.Embed(title="Gamble")
                    bet_embed.set_author(name=ctx.author.name)
                    bet_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                    bet_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    bet_embed.add_field(name="** **", value="** **", inline=False)
                    bet_embed.add_field(name=f"CONGRATS!! YOU HIT JACKPOT", value=f"YOU EARNED ``{numberate(jackpotAmount - amount)} coins``!! Your new balance is ``{numberate(balresult)} coins``", inline=False)
                    bet_embed.add_field(name="** **", value="** **", inline=False)

                    await ctx.send(embed=bet_embed)
    
def setup(client):
    client.add_cog(Bet(client))