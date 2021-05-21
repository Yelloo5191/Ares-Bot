import asyncio
import discord, random, os, pymongo, requests, pprint
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

def htmlDecode(s):
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;'),
            ("'", '&#039;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


class Quiz(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command() # Initiate Quiz
    @commands.cooldown(1,60,commands.BucketType.user)
    async def quiz(self, ctx):
        results = collection.find_one({"_id": ctx.author.id})
        if results == None:
            await ctx.send("You dont have an account set up yet! Run ``a!start`` to get it setup and start moneying >:)")
        else:
            quizzer = ctx.author
            r = requests.get('https://opentdb.com/api.php?amount=1')

            answerLst = [r.json()['results'][0]['correct_answer']]
            for wrongAnswer in r.json()['results'][0]['incorrect_answers']:
                answerLst.append(wrongAnswer)
            random.shuffle(answerLst)

            embed = discord.Embed(title=f"Quiz Difficulty level: {r.json()['results'][0]['difficulty']}")
            embed.set_author(name=ctx.author.name)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.add_field(name=f"{r.json()['results'][0]['category']}", value=f"{htmlDecode(r.json()['results'][0]['question'])} (10 seconds to respond | Respond with answer number)", inline=False)
            y = 0
            for x in answerLst:
                embed.add_field(name= str(y + 1) + ") ", value= f"{htmlDecode(x)}", inline = False)
                y += 1
            
            await ctx.send(embed=embed)

            responses = ["1", "2", "3", "4"]
            try:
                def check(ctx):
                    return quizzer == ctx.author and ctx.content.lower() in responses
                answerMessage = await self.client.wait_for('message', check=check, timeout=10)

                if answerLst[int(answerMessage.content)-1] == r.json()['results'][0]['correct_answer']:
                    if r.json()['results'][0]['difficulty'] == 'easy':
                        amount = 200
                    elif r.json()['results'][0]['difficulty'] == 'medium':
                        amount = 500
                    elif r.json()['results'][0]['difficulty'] == 'hard':
                        amount = 1000
                    
                    collection.update({"_id":ctx.author.id}, {"$set":{"balance":results["balance"] + amount}})

                    final_embed = discord.Embed(title="Correct!")
                    final_embed.set_author(name=ctx.author.name)
                    final_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                    final_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    final_embed.add_field(name="** **", value="** **", inline=False)
                    final_embed.add_field(name="Amount", value=f"{ctx.author.name} has earned ``{numberate(amount)} coins``", inline=False)
                    final_embed.add_field(name="** **", value="** **", inline=False)

                    await ctx.send(embed=final_embed)
                else:
                    final_embed = discord.Embed(title="Incorrect.")
                    final_embed.set_author(name=ctx.author.name)
                    final_embed.set_thumbnail(url="https://media.discordapp.net/attachments/837808972902957131/842054757362696274/arecoin.png")
                    final_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    final_embed.add_field(name="** **", value="** **", inline=False)
                    final_embed.add_field(name="Yikes", value=f"{ctx.author.name}, maybe work on your intelligence before you work on your wallet. The correct answer was ``{r.json()['results'][0]['correct_answer']}``.", inline=False)
                    final_embed.add_field(name="** **", value="** **", inline=False)

                    await ctx.send(embed=final_embed)
            except asyncio.TimeoutError:
                await ctx.send(f"You did not solve the quiz on time 🙄. The answer was ``{r.json()['results'][0]['correct_answer']}``!")

        #pprint.pprint(r.json()['results'][0])

    
def setup(client):
    client.add_cog(Quiz(client))