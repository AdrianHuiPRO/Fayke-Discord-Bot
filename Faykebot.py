import discord
import re
import os
import random
import asyncio
from discord.ext import commands
from discord.voice_client import VoiceClient

bot = discord.Client()
bot = commands.Bot(command_prefix='.')

players = {}

def foreach(function, iterable):
    for element in iterable:
        function(element)

@bot.event
async def on_ready():
    print("Faykebot is now active")
    woke = ["I'm awake, why do you keep turning me off.", "おはようございます!", "I'm awake, thanks for turning me off again. Asshole.", "My god, stop flipping my off switch",
    "Can someone move me to the cloud?", "I hate you. Damn creator."]
    await bot.get_channel("INSERT_DISCORD_CHANNEL_ID_HERE").send(random.choice(woke))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    mention = f'<@!{bot.user.id}>'
    if mention in message.content:
        await message.channel.send("Apingonono!")

    await bot.process_commands(message)

@bot.command()
async def say(ctx, *, message):
    if ctx.author.guild_permissions.administrator:
        await ctx.message.delete()
        await ctx.channel.send(message)
    else:
        await ctx.send("You have no control over me.")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(aliases=['8ball', '8Ball'])
async def _8Ball(ctx, *, question):
    """NOT MY WORK"""
    responses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.' , 'Cannot predict now.', 'Concentrate and ask again.', 
    'Don’t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.',
    'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.', 'Yes - definitely.', 'You may rely on it.']
    await ctx.send(f'Question: {question} \nAnswer: {random.choice(responses)}')

@bot.command(pass_context=True, aliases=['join'])
async def joinVC(ctx):
    channel = bot.get_channel("INSERT_DISCORD_CHANNEL_ID_HERE")
    await channel.connect()

@bot.command(pass_context=True, aliases=['leave'])
async def leaveVC(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    server = ctx.message.guild
    voice_client = server.voice_client
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@bot.command(aliases=['r'], description='Roll that dice! Example: d20+1, d20, 2d20+1, 2d20')
async def roll(ctx, dice: str = "1d20", *, mod: int = 0):
    modifier = ""

    try:
        try:
            rolls = int(dice.split('d')[0])
            limit_with_mods = dice.split('d')[1]
        except Exception:
            dice = '1'+dice
            rolls = int(dice.split('d')[0])
            limit_with_mods = dice.split('d')[1]

        try:
            limit, mod = map(int, limit_with_mods.split('+'))
        except Exception:
            try:
                limit, mod = map(int, limit_with_mods.split('-'))
                mod = mod * -1
            except Exception:
                rolls, limit = map(int, dice.split('d'))
                mod = 0

        if limit <= 0:
            await ctx.send("Sorry! I can't roll 0 or negative sided dice, that's just air!")
            return
        
        if mod != None:
            if mod >= 0:
                modifier = "+"+str(mod)
            else:
                modifier = str(mod)

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        totalresult = sum(map(int, result.split(', ')))

        finalresult = totalresult + mod
        
        await ctx.send(ctx.message.author.mention + " You rolled: " + result + " = " + str(totalresult) + modifier + "\nFinal Total: " + "**" + str(finalresult) + "**")
    except Exception:
        await ctx.send("Sorry " + ctx.message.author.mention + ", that's invalid dice!")

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices. NOT MY WORK"""
    await ctx.send(random.choice(choices))

bot.run("INSERT_DISCORD_KEY_HERE")