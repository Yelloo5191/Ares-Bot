from re import X
import discord, random, os, pymongo
from discord.ext import commands
from discord.ext.commands import has_permissions
from pymongo import MongoClient

# - Token hiding thing
from dotenv import load_dotenv

load_dotenv()

prefix = 'a!'
client = commands.Bot(command_prefix=prefix, help_command=None, case_insensitive=True)
client.remove_command('help')
self_id = 837809072539566121


# - Mongo Setup
cluster = MongoClient(os.getenv("MONGO_TOKEN"))
db = cluster["ares"]
collection = db["economy"]


# - Loads cogs
for filename in os.listdir('./cogs/economy'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.economy.{filename[:-3]}')

# - Function for adding ',' in numbers
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


# - Bot Status Events and Commands
@client.event
async def on_ready():
    activity = discord.Game(name="In Development | a!help")
    await client.change_presence(status=discord.Status.dnd, activity=activity)
    print("Bot is online")

# - Ping command to check latency
@client.command()
@has_permissions(administrator = True)
async def ping(ctx):
    await ctx.send(f"{ctx.author.mention} pong!\nThe response time for your ping was ``{round(client.latency * 1000)}ms``")


@client.event  # - Error handling
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, you are lacking the permissions required for running this command. If you believe this is an error, message an Admin or Dev.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.name}, you are lacking a required parameter/argument. Please enter all the required args or refer to a!help.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.name}, this command was not found, check your spelling and capitalization and try again or refer to a!help.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(f"{ctx.author.name}, you entered an extra/incorrect paramater, try again or refer to a!help")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"{ctx.author.name}, you entered an extra/incorrect paramater, try again or refer to a!help")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.name}, that command is on cooldown, please wait ``{round(error.retry_after)} seconds``!")
    else:
        await ctx.send("An unexpected error occurred.")
        raise error



@client.command() # - Command to edit econ database directly 
async def setbal(ctx, amount: int, user: discord.Member = None):
    if ctx.author.id == 304024578009595907: # checks if its me
        if user == None:
            user = ctx.author
        results = collection.find_one({"_id": user.id})
        if results == None:
            await ctx.send("You or the member mentioned dont have an account set up yet! Run ``a!start`` to get it setup and start moneying >:)")
        else:
            collection.update_one({"_id": user.id}, {"$set":{"balance":amount}})
            results = collection.find_one({"_id": user.id})
            balresult = results["balance"]

            setbal_embed = discord.Embed(title="Set Balance")
            setbal_embed.set_author(name=ctx.author.name)
            setbal_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
            setbal_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            setbal_embed.add_field(name="** **", value="** **", inline=False)
            setbal_embed.add_field(name=f"Bal {user.name}'s", value=f"balance has been set to ``{numberate(balresult)} coins``", inline=False)
            setbal_embed.add_field(name="** **", value="** **", inline=False)

            await ctx.send(embed=setbal_embed)
    else:
        await ctx.send("You can't do that weirdo 🤨")
    


# - Help command group
@client.group(invoke_without_command=True)
async def help(ctx):
    he = discord.Embed(title="Ares Help", description="Use a!help <command> for more specific help on a command")

    he.add_field(name = "Economy", value="**start, leaderboard, bal,\n\n daily, pay, bet,\n\n fight, quiz, beg**")
    he.add_field(name = "Misc", value="**ping**")
    he.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he)

# - Help command subgroups
@help.command()
async def start(ctx):
    he1 = discord.Embed(title="Start", description="Starts your economy and banking account for Ares Economy")

    he1.add_field(name = "----\na!\n----", value="usage: start")
    he1.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he1)

@help.command()
async def bal(ctx):
    he2 = discord.Embed(title="Bal", description="Checks the balance of the user mentioned, if none are mentioned then the balance of the author is sent")

    he2.add_field(name = "----\na!\n----", value="usage: bal [@user]")
    he2.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he2)

@help.command()
async def pay(ctx):
    he3 = discord.Embed(title="Pay", description="Pays the mentioned user amount specified")

    he3.add_field(name = "----\na!\n----", value="usage: pay <@user> <amount>")
    he3.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he3)

@help.command()
async def bet(ctx):
    he4 = discord.Embed(title="Bet", description="Gambles amount of money specified for a chance to double up or lose it all \n There is also an extremely small chance at hitting jackpot")

    he4.add_field(name = "----\na!\n----", value="usage: bet <amount>")
    he4.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he4)

@help.command()
async def fight(ctx):
    he5 = discord.Embed(title="Fight", description="Sets a fight with mentioned user. Winner takes bet amount.")

    he5.add_field(name = "----\na!\n----", value="usage: fight <player> <amount>")
    he5.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he5)

@help.command()
async def leaderboard(ctx):
    he6 = discord.Embed(title="Leaderboard", description="Displays global leaderboard.")

    he6.add_field(name = "----\na!\n----", value="usage: leaderboard")
    he6.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he6)

@help.command()
async def ping(ctx):
    he6 = discord.Embed(title="Ping", description="Pings the bot and returns the response time in milliseconds.")

    he6.add_field(name = "----\na!\n----", value="usage: ping")
    he6.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he6)

@help.command()
async def daily(ctx):
    he7 = discord.Embed(title="Daily", description="Claims the daily rewards for the author of the command.")

    he7.add_field(name = "----\na!\n----", value="usage: daily")
    he7.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he7)

@help.command()
async def quiz(ctx):
    he7 = discord.Embed(title="Quiz", description="Starts a quiz, get the correct answer and you earn money.")

    he7.add_field(name = "----\na!\n----", value="usage: quiz")
    he7.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = he7)

@help.command()
async def beg(ctx):
    embed = discord.Embed(title="Beg", description="Initiates a beg for money.")

    embed.add_field(name = "----\na!\n----", value="usage: beg")
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

    await ctx.send(embed = embed)


client.run(os.getenv("TOKEN"))