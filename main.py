#!/usr/bin/python3
'''BossBot: An adaptable Discord bot written in Python.
This file contains all functions that need direct interaction with Discord.'''
import asyncio
import config_handler
import neatStuff
import discord
from discord.ext import commands
import logging

logging.basicConfig(level = logging.INFO)

bot_prefix = '$' #this is the prefix to be used in a Discord channel to get the bot's attention
description = 'Hello! I can do many things, like the stuff below. Get my attention with %s' %bot_prefix
botStatus = ''
config = {}

bot = commands.Bot(description=description, command_prefix=bot_prefix) #create an instance of Bot

async def memeHandler(context):
    '''performs the appropriate action based on what neatStuff.sendMeme() returns'''
    meme = neatStuff.sendMeme()
    if meme[:2] == './':
        print('sending meme %s' %meme)
        await bot.send_file(context.message.channel, meme)
        print('%s was successfully uploaded' %meme)
    elif meme == 'no memes':
        await bot.send_message(context.message.channel, 'I don\'t have any memes. Try sending me some with %suploadMeme!' %bot_prefix)
    else:
        print('An error occured when trying to send a meme.')

async def downloadMeme(context):
    '''saves the attachments in an attachment list'''
    URLs = []
    filenames = []
    for attachment in context.message.attachments:
        URLs.append(attachment['url'])
        filenames.append(attachment['filename'])
        result = neatStuff.downloadMeme(URLs, filenames)
        if result == 0:
            await bot.send_message(context.message.channel, '%s was added to my meme repository' %attachment['filename'])
        elif result == 1:
            await bot.send_message(context.message.channel, 'This file type is not allowed. Please only upload GIFs, JPEGs, or PNGs.')
        elif result == 2:
            await bot.send_message(context.message.channel, 'I already have this meme!')

async def getIcon(context):
    '''send the avatar urls of the mentioned users in a message, to be used with icon command
    Preconditions: context, which is the context the message is sent with'''
    if len(context.message.mentions) == 0:
        await bot.send_message(context.message.channel, 'Make sure to mention a user(s) after using this command!')
    else:
        for member in context.message.mentions:
            await bot.send_message(context.message.channel, 'Icon of %s: %s' %(member.mention, member.avatar_url))

async def searchGoogle(context, searchParameters=''):
    '''search Google for the applicable term in a message
    Preconditions: context, which is the context the message is sent with. searchParameters, to prepend the actual search term with.'''
    if len(context.message.content) <= 8:
        await bot.send_message(context.message.channel, 'Make sure to give me something to search for after using this command!')
    else:
        for result in neatStuff.searchGoogle(searchParameters + context.message.content[8:]):
            await bot.send_message(context.message.channel, result)

@bot.event
async def on_ready():
    '''prints Discord login information and version info to console when the bot has logged in'''
    print('\n==INITIALIZATION COMPLETE==')
    print('BossBot is logged in')
    print('Username: %s' %bot.user.name)
    print('ID: %s' %str(bot.user.id))
    print('Running on Discord.py ' + discord.__version__)
    await bot.change_presence(game = discord.Game(name = botStatus))

@bot.command(pass_context=True) #passes context from command
async def ping(context):
    '''play pong'''
    await bot.send_message(context.message.channel, 'Pong!')

@bot.command(pass_context=True)
async def sergals(context):
    '''get an interesting sergal fact'''
    await bot.send_message(context.message.channel, neatStuff.sendSergalFact())

@bot.command(pass_context=True)
async def dice(context):
    '''roll a dice'''
    await bot.send_message(context.message.channel, '%s rolled a %d' %(context.message.author.mention, neatStuff.rollDice()))

@bot.command(pass_context=True)
async def death(context):
    '''find out when you will die'''
    await bot.send_message(context.message.channel, neatStuff.deathclock())

@bot.command(pass_context=True)
async def meme(context):
    '''sends a meme to the channel'''
    await memeHandler(context)

@bot.command(pass_context=True)
async def uploadMeme(context):
    '''upload a meme for me to add to the meme command'''
    await downloadMeme(context)

@bot.command(pass_context=True)
async def icon(context):
    '''When no arguments are given, return the bot's icon. When a valid user is given, return the user's icon.'''
    await getIcon(context)

@bot.command(pass_context=True)
async def fullwidth(context):
    '''convert your message into Unicode Fullwidth'''
    await bot.send_message(context.message.channel, neatStuff.fullwidth(context.message.content[11:]))

@bot.command(pass_context=True)
async def google(context):
    '''search Google'''
    await bot.send_message(context.message.channel, 'Searching Google for %s...' %context.message.content[8:])
    await searchGoogle(context)

@bot.command(pass_context=True)
async def youtube(context):
    '''search Google for YouTube videos'''
    await bot.send_message(context.message.channel, 'Searching YouTube for %s...' %context.message.content[9:])
    await searchGoogle(context, 'site:youtube.com ')

@bot.command(pass_context=True)
async def wikipedia(context):
    '''search Wikipedia'''
    await bot.send_message(context.message.channel, neatStuff.searchWikipedia(context.message.content[11:]))

@bot.command(pass_context=True)
async def source(context):
    '''get a link to my GitHub repo'''
    await bot.send_message(context.message.channel, 'https://github.com/CoolDude311/BossBot')

@bot.command(pass_context=True)
async def invite(context):
    '''use this to receive a link to add me to your server'''
    await bot.send_message(context.message.channel, 'PMing %s an invite link...' %context.message.author.mention)
    await bot.send_message(context.message.author, discord.utils.oauth_url(bot.user.id))

def init():
    '''Imports the configuration and starts the bot'''
    global config
    global botStatus
    config = config_handler.checkConfig()
    botStatus = input('What would you like the bot\'s status to be? ')
    print('\nLogging in...')
    bot.run(config["api_keys"]["discord"]) #login to Discord using a Bot API in place of token

if __name__ == '__main__':
    init()
