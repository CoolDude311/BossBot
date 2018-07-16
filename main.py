#!/usr/bin/python3
'''BossBot: An adaptable Discord bot written in Python.
This file contains all functions that need direct interaction with Discord.'''
from apis import *
import asyncio
import config_handler
import neatStuff
import discord
from discord.ext import commands
import logging
from random import choice, randint
from sys import exit

logging.basicConfig(level = logging.INFO)

bot_prefix = '$' #this is the prefix to be used in a Discord channel to get the bot's attention
description = 'Hello! I can do many things, like the stuff below. Get my attention with %s' %bot_prefix
botStatus = ''
config = {}
youtube_handler = False

colours = [discord.Colour.teal(), discord.Colour.dark_teal(), discord.Colour.green(), discord.Colour.dark_green(), discord.Colour.blue(), discord.Colour.dark_blue(), discord.Colour.purple(), discord.Colour.dark_purple(), discord.Colour.magenta(), discord.Colour.dark_magenta(), discord.Colour.gold(), discord.Colour.dark_gold(), discord.Colour.orange(), discord.Colour.dark_orange(), discord.Colour.red(), discord.Colour.dark_red()]

bot = commands.Bot(description=description, command_prefix=bot_prefix) #create an instance of Bot
bot.remove_command("help")

@bot.event
async def on_ready():
    '''prints Discord login information and version info to console when the bot has logged in'''
    print('\n==INITIALIZATION COMPLETE==')
    print('BossBot is logged in')
    print('Username: %s' %bot.user.name)
    print('ID: %s' %str(bot.user.id))
    print('Running on Discord.py ' + discord.__version__)
    if len(botStatus) > 0:
        await bot.change_presence(game = discord.Game(name = botStatus))

@bot.command(pass_context=True)
async def help(context):
    embed = discord.Embed(title="Help", colour = discord.Colour.dark_purple())
    embed.add_field(name="death", value="find out when you will die", inline=False)
    embed.add_field(name="dice", value="roll a dice", inline=False)
    embed.add_field(name="fullwidth", value="convert some text to fullwidth", inline=False)
    embed.add_field(name="invite", value="get a link that lets you add me to your server", inline=False)
    embed.add_field(name="meme", value="get a random meme", inline=False)
    embed.add_field(name="uploadmeme", value="give me a meme for me to use with the meme command. To use it, send an image and put this command in the caption", inline=False)
    embed.add_field(name="sergals", value="get a random sergal fact", inline=False)
    embed.add_field(name="wikipedia", value="search Wikipedia", inline=False)
    embed.add_field(name="youtube", value="search YouTube", inline=False)
    embed.add_field(name="about", value="Get information about this bot", inline=False)
    await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True) #passes context from command
async def ping(context):
    '''play pong'''
    await bot.send_message(context.message.channel, embed=discord.Embed(title="Pong!", colour=choice(colours)))

@bot.command(pass_context=True)
async def sergals(context):
    '''get an interesting sergal fact'''
    embed = discord.Embed(title="Sergal Fact #" + str(randint(1, 100)), description=neatStuff.sendSergalFact(), colour=choice(colours))
    await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True)
async def dice(context):
    '''roll a dice'''
    embed = discord.Embed(title='%s rolled a %d' %(context.message.author.name, neatStuff.rollDice()), colour=choice(colours))
    embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
    await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True)
async def death(context):
    '''find out when you will die'''
    embed = discord.Embed(title=neatStuff.deathclock(), colour=choice(colours))
    embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
    await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True)
async def meme(context):
    '''sends a meme to the channel'''
    meme = neatStuff.sendMeme()
    if meme[:2] == './':
        await bot.send_file(context.message.channel, meme)
    elif meme == 'no memes':
        embed = discord.Embed(title="I don't have any memes. Try sending me some with %suploadMeme" %bot_prefix, colour=choice(colours))
        await bot.send_message(context.message.channel, embed=embed)
    else:
        print('An error occured when trying to send a meme.')

@bot.command(pass_context=True)
async def uploadMeme(context):
    '''upload a meme for me to add to the meme command'''
    URLs = []
    filenames = []
    for attachment in context.message.attachments:
        URLs.append(attachment['url'])
        filenames.append(attachment['filename'])
        result = await neatStuff.downloadImage(URLs, filenames)
        print("result:", result)
        if result == 0:
            await bot.send_message(context.message.channel, embed=discord.Embed(title='%s was added to my meme repository' %attachment['filename'], colour=choice(colours)))
        elif result == 1:
            await bot.send_message(context.message.channel, embed=discord.Embed(title='This file type is not allowed. Please only upload GIFs, JPEGs, or PNGs.', colour=choice(colours)))
        elif result == 2:
            await bot.send_message(context.message.channel, embed=discord.Embed(title='I already have this meme!', colour=choice(colours)))

@bot.command(pass_context=True)
async def icon(context):
    '''When no arguments are given, return the bot's icon. When a valid user is given, return the user's icon.'''
    if len(context.message.mentions) == 0:
        await bot.send_message(context.message.channel, embed=discord.Embed(title='Make sure to mention a user(s) after using this command!', colour=choice(colours)))
    else:
        for member in context.message.mentions:
            embed = discord.Embed(title="Icon of " + member.name, colour=choice(colours))
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_image(url=member.avatar_url)
            await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True)
async def fullwidth(context):
    '''convert your message into Unicode Fullwidth'''
    embed = discord.Embed(title=neatStuff.fullwidth(context.message.content[11:]), colour=discord.Colour.purple())
    embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
    await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True)
async def youtube(context):
    '''search for YouTube videos'''
    if youtube != False:
        try:
            for result in youtube_handler.video_search(context.message.content[9:], 1):
                await bot.send_message(context.message.channel, result.url)
        except ImportError:
            print("An error occured when searching YouTube. It may be alright.")
    else:
        embed = discord.Embed(title="YouTube functionality has not been enabled. Please talk to my owner.", colour=discord.Colour.dark_red())
        embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
        await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True)
async def wikipedia(context):
    '''search Wikipedia'''
    await bot.send_message(context.message.channel, wikipedia_search(context.message.content[11:]))

@bot.command(pass_context=True)
async def about(context):
    '''get a link to my GitHub repo'''
    embed = discord.Embed(title="About this bot", description="This bot was a final project of sorts for my Python course. I've been adding to it since then.\nI'm still a fairly inexperienced developer, so apologies for any bugs you experience. Feel free to contact me with any problems you're having, or create an issue on the GitHub repo. No promises as to when I'll be able to look into it though.\nThank you for using my bot!", colour=discord.Colour.dark_purple())
    embed.add_field(name="Discord", value="Xena#6395", inline=False)
    embed.add_field(name="Twitter", value="https://twitter.com/Pbod64", inline=False)
    embed.add_field(name="tumblr", value="https://xenusprophet.tumblr.com", inline=False)
    embed.add_field(name="GitHub Repository", value="https://github.com/CoolDude311/BossBot", inline=False)
    await bot.send_message(context.message.channel, embed=embed)

@bot.command(pass_context=True)
async def invite(context):
    '''use this to receive a link to add me to your server'''
    await bot.send_message(context.message.author, discord.utils.oauth_url(bot.user.id))

if __name__ == '__main__':
    config = config_handler.checkConfig()
    if config["youtube_settings"]["youtube_enabled"]:
        youtube_handler = YoutubeSearch(config["api_keys"]["youtube"])
    botStatus = input('What would you like the bot\'s status to be? ')
    while True:
        try:
            print("Logging in...")
            bot.loop.run_until_complete(bot.start(config["api_keys"]["discord"]))
        except KeyboardInterrupt:
            print("\nLogging off...")
            bot.logout()
            bot.close()
            print("Successfully exited. Thank you for using BossBot.")
            exit(0)
        except Exception as error:
            print("Error:", error)
            print("Attempting restart...")
            bot.loop.run_until_complete(bot.logout())
            for task in asyncio.Task.all_tasks(loop=bot.loop):
                if task.done():
                    task.exception()
                    continue
                task.cancel()
                try:
                    bot.loop.run_until_complete(asyncio.wait_for(task, 5, loop=bot.loop))
                    task.exception()
                except asyncio.InvalidStateError:
                    pass
                except asyncio.TimeoutError:
                    pass
                except asyncio.CancelledError:
                    pass
            bot = discord.Client(loop=bot.loop)