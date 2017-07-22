#!/usr/bin/python3
'''BossBot: An adaptable Discord bot written in Python
Author: William Harrell'''
import asyncio
import configHandler
import neatStuff
import discord
from discord.ext import commands

description = 'This is a Discord bot I have written to prove my Python capabilities to my instructors. Research used during the construction of this bot can be found at the end of "main.py" in the project. The name "BossBot" comes from a character in Metal Gear Solid.'
bot_prefix = '$' #this is the prefix to be used in a Discord channel to get the bot's attention

bot = commands.Bot(description=description, command_prefix=bot_prefix) #create an instance of Bot

@bot.event
async def on_ready():
    '''prints Discord login information and version info to console when the bot has logged in'''
    print('BossBot is logged in, reporting for duty!')
    print('Username: %s' %bot.user.name)
    print('ID: %s' %str(bot.user.name))
    print('Running on Discord.py ' + discord.__version__)

@bot.command(pass_context=True) #passes context from command
async def ping(context):
    '''respond to "ping" with "Pong!"'''
    await bot.say('Pong!')

@bot.command(pass_context=True)
async def sergals(context):
    '''respond to "sergals" with "are excessively floofy"'''
    await bot.say('are excessively floofy')

@bot.command(pass_context=True)
async def dice(context):
    '''respond to "dice" with a roll of the dice from neatStuff.rollDice()'''
    await bot.say('You rolled a %d' %neatStuff.rollDice(6))

def init():
    '''Imports the configuration from "./config/main.conf" and starts the bot'''
    mainConfig = configHandler.checkConfig()
    bot.run('token') #login to Discord using a Bot API in place of token

init()

'''
Research used:
    Discord bot beginning tutorial (used for learning how to initially set up the bot, and what additional skills would need to be gained before the bot could be written: https://youtu.be/bYfhQODnH0g
    Discord.py Documentation: https://discordpy.readthedocs.io/en/latest/api.html#client
    Video on Python Decorators: https://youtu.be/mZ5IwFfqvz8
'''
