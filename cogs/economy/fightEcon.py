import asyncio
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

class Fight(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command() # Intiates Gamble Fight
    async def fight(self, ctx, user: discord.Member, amount):
        amount = int(amount)
        results = collection.find_one({"_id": user.id})
        results2 = collection.find_one({"_id": ctx.author.id})
        if results == None or results2 == None:
            await ctx.send("You or the member mentioned dont have an account set up yet! Run ``a!start`` to get it setup and start moneying >:)")
        else:
            if amount > results["balance"] or amount > results["balance"]:
                await ctx.send("You or the member mentioned do not have the available balance to make that bet")
            else:
                responses = ["y", "n"]
                fought = user
                attacker = ctx.author
                if user.id == ctx.author.id:
                    await ctx.send("You can't fight yourself weirdo")
                else:
                    try:
                        await ctx.send(user.mention + ", " + ctx.author.mention + " has challenged you to a duel, do you accept? ``(Y/N)``")
                        def check(ctx):
                            return fought == ctx.author and ctx.content.lower() in responses
                        answerMessage = await self.client.wait_for('message', check=check, timeout=60.0)
                        if answerMessage.content.lower() == "y":
                            await ctx.send("Duel invite accepted! Fight will now begin.")
                            fightStart = True
                        elif answerMessage.content.lower() == "n":
                            await ctx.send('Duel invite declined.')
                            fightStart = False
                    except asyncio.TimeoutError:
                        await ctx.send('Duel invite expired.')
                        fightStart = False
                        
                    
                if fightStart: 
                    player1health = 100
                    player2health = 100
                    player1defense = 0
                    player2defense = 0
                    fightOn = True
                    while fightOn:
                        #Player 1 Attack
                        playerCheck = attacker
                        responses = ["fight", "heal", "defend"]
                        await ctx.send(f"{ctx.author.mention} Choose your action\n``Fight``   ``Heal``   ``Defend``")
                        def checkFight(ctx):
                            return playerCheck == ctx.author and ctx.content.lower() in responses
                        answerMessage = await self.client.wait_for('message', check=checkFight, timeout=60.0)
                        try:
                            if answerMessage.content.lower() == 'fight':
                                attackDamage = random.randint(0,51)
                                player2health -= attackDamage
                                await ctx.send(f"{ctx.author.mention} attacked with ``{attackDamage}`` damage! {user.mention} is left with ``{player2health}`` health!")
                            elif answerMessage.content.lower() == 'defend': 
                                if player1defense >= 30:
                                    await ctx.send("You are at max defense")
                                else:
                                    defendAmount = random.randint(0,11)
                                    player1defense += defendAmount
                                await ctx.send(f"{ctx.author.mention} upgraded their defense to ``{defendAmount}``!")
                            elif answerMessage.content.lower() == 'heal':
                                if player1health >= 100:
                                    ctx.send("You are at max health")
                                else:
                                    healAmount = random.randint(0,11)
                                    await ctx.send(f"{ctx.author.mention} healed ``{healAmount}`` health!")
                                    player1health += healAmount
                        except asyncio.TimeoutError:
                            ctx.send("Coward. The duel is over due to no response.")
                            fightStart = False
                            fightOn = False

                        if player2health <= 0:
                            loser = collection.find_one({"_id":user.id})
                            winner = collection.find_one({"_id":ctx.author.id})

                            collection.update_one({"_id":user.id}, {"$set":{"balance":loser["balance"]-amount}})
                            collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":winner["balance"]+amount}})

                            loser = collection.find_one({"_id":user.id})
                            winner = collection.find_one({"_id":ctx.author.id})

                            loserbal = loser["balance"]
                            winnerbal = winner["balance"]

                            await ctx.send(f"{user.mention} ``has lost to`` {ctx.author.mention} ``who is left with {player1health} health!``")
                            await ctx.send(f"As a result, {ctx.author.mention} earned ``{numberate(amount)} coins`` with a current balance of ``{numberate(winnerbal)} coins`` and {user.mention} lost ``{numberate(amount)} coins`` leaving them with a current balance of ``{numberate(loserbal)} coins``")
                            fightStart = False
                            fightOn = False
                            break
                        
                        #Player 2 Attack
                        playerCheck = fought
                        responses = ["fight", "heal", "defend"]
                        await ctx.send(f"{user.mention} Choose your action\n``Fight``   ``Heal``   ``Defend``")

                        answerMessage = await self.client.wait_for('message', check=checkFight, timeout=60.0)
                        try:
                            if answerMessage.content.lower() == 'fight':
                                attackDamage = random.randint(0,51)
                                player1health -= attackDamage
                                await ctx.send(f"{user.mention} attacked with ``{attackDamage}`` damage! {ctx.author.mention} is left with ``{player1health}`` health!")
                            elif answerMessage.content.lower() == 'defend': 
                                if player2defense >= 30:
                                    await ctx.send("You are at max defense")
                                else:
                                    defendAmount = random.randint(0,11)
                                    player2defense += defendAmount
                                await ctx.send(f"{user.mention} upgraded their defense to ``{defendAmount}``!")
                            elif answerMessage.content.lower() == 'heal':
                                if player2health >= 100:
                                    ctx.send("You are at max health")
                                else:
                                    healAmount = random.randint(0,11)
                                    await ctx.send(f"{user.mention} healed ``{healAmount}`` health!")
                                    player2health += healAmount
                        except asyncio.TimeoutError:
                            ctx.send("Coward. The duel is over due to no response.")
                            fightStart = False
                            fightOn = False
                            
                        if player1health <= 0:
                            loser = collection.find_one({"_id":ctx.author.id})
                            winner = collection.find_one({"_id":user.id})

                            collection.update_one({"_id":ctx.author.id}, {"$set":{"balance":loser["balance"]-amount}})
                            collection.update_one({"_id":user.id}, {"$set":{"balance":winner["balance"]+amount}})

                            loser = collection.find_one({"_id":ctx.author.id})
                            winner = collection.find_one({"_id":user.id})

                            loserbal = loser["balance"]
                            winnerbal = winner["balance"]

                            await ctx.send(f"{ctx.author.mention} ``has lost to`` {user.mention} ``who is left with {player2health} health!``")
                            await ctx.send(f"As a result, {user.mention} earned ``{numberate(amount)} coins`` with a current balance of ``{numberate(winnerbal)} coins`` and {ctx.author.mention} lost ``{numberate(amount)} coins`` leaving them with a current balance of ``{numberate(loserbal)} coins``")
                            fightStart = False
                            fightOn = False
                            break
    
def setup(client):
    client.add_cog(Fight(client))