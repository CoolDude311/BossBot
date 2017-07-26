#!/usr/bin/python3
'''BossBot: An adaptable Discord bot written in Python.
This file contains all functions that need direct interaction with Discord.
Author: William Harrell'''
import asyncio
import configHandler
import neatStuff
import discord
from discord.ext import commands

description = 'This is a Discord bot I have written to prove my Python capabilities to my instructors. Research used during the construction of this bot can be found at the end of "main.py" in the project. The name "BossBot" comes from a character in Metal Gear Solid.'
bot_prefix = '$' #this is the prefix to be used in a Discord channel to get the bot's attention

bot = commands.Bot(description=description, command_prefix=bot_prefix) #create an instance of Bot

async def memeHandler(context):
    '''performs the appropriate action based on what neatStuff.sendMeme() returns'''
    meme = neatStuff.sendMeme()
    if meme[:2] == './':
        print('sending meme %s' %meme)
        await bot.send_file(context.message.channel, meme)
        print('%s was successfully uploaded')
    elif meme == 'no memes':
        await bot.send_message(context.message.channel, 'I don\'t have any memes. Try sending me some!')
    else:
        print('An error occured when trying to send a meme.')

@bot.event
async def on_ready():
    '''prints Discord login information and version info to console when the bot has logged in'''
    print('\n==INITIALIZATION COMPLETE==')
    print('BossBot is logged in, reporting for duty!')
    print('Username: %s' %bot.user.name)
    print('ID: %s' %str(bot.user.id))
    print('Running on Discord.py ' + discord.__version__)

@bot.command(pass_context=True) #passes context from command
async def ping(context):
    '''respond to "ping" with "Pong!"'''
    await bot.send_message(context.message.channel, 'Pong!')

@bot.command(pass_context=True)
async def sergals(context):
    '''respond to "sergals" with "are excessively floofy"'''
    await bot.send_message(context.message.channel, 'are excessively floofy')

@bot.command(pass_context=True)
async def dice(context):
    '''respond to "dice" with a roll of the dice from neatStuff.rollDice()'''
    await bot.send_message(context.message.channel, '%s rolled a %d' %(context.message.author.mention, neatStuff.rollDice()))

@bot.command(pass_context=True)
async def death(context):
    '''respond to "death" with an appropriate message telling the user when they will die'''
    await bot.send_message(context.message.channel, neatStuff.deathclock())

@bot.command(pass_context=True)
async def meme(context):
    '''sends a meme to the channel'''
    await memeHandler(context)

@bot.command(pass_context=True)
async def icon(context):
    '''When no arguments are given, return the bot's icon. When a valid user is given, return the user's icon.'''
    await bot.say(str(discord.AppInfo.icon_url))

@bot.command(pass_context=True)
async def invite(context):
    '''pm the user an invite'''
    await bot.send_message(context.message.channel, 'PMing %s an invite link...' %context.message.author.mention)
    await bot.send_message(context.message.author, discord.utils.oauth_url(bot.user.id))

def init():
    '''Imports the configuration from "./config/main.conf" and starts the bot'''
    configHandler.makeConfig()
    apiKeys = configHandler.readApiKeys()
    print('Discord API Key: %s' %apiKeys[0])
    bot.run(str(apiKeys[0])) #login to Discord using a Bot API in place of token

if __name__ == '__main__':
    init()

'''
Research used:
    Discord bot beginning tutorial (used for learning how to initially set up the bot, and what additional skills would need to be gained before the bot could be written: https://youtu.be/bYfhQODnH0g
    Discord.py Documentation: https://discordpy.readthedocs.io/en/latest/api.html#client
    Video on Python Decorators: https://youtu.be/mZ5IwFfqvz8
'''
