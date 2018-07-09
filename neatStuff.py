#!/usr/bin/env python3
'''This module contains functions to be used as responses in main.py'''
import aiohttp
import os
import random
import re
#import urllib.request

acceptableFileTypes = re.compile('jpeg|jpg|png|gif')
headers = {"User-Agent":"BossBot/v1.5"}
sergalFacts = ['Sergals are excessively floofy.', 'Sergals are made of cheese.', 'Sergals originally came from the moon, because, like the moon, they are made of cheese.', 'Sergals are actually just floofy land sharks.', 'Sergals are börk sharks.']

def rollDice(dieSides=6):
    '''Preconditions: an integer (dieSides). Default is 6.
    Postconditions: returns an integer between 1 and dieSides.'''
    return random.randint(1, dieSides)

def deathclock():
    '''Returns a number between 1 and 100, and matches it to the appropriate phrase.'''
    years = random.randint(1, 100)
    if years > 30:
        return 'Sorry friend, you still have %d years to suffer through.' %years
    elif years > 20 and years <= 30:
        return 'Not too bad, %d years left.' %years
    elif years > 10 and years <= 20:
        return 'Congratulations, only %d more years to go of this disgusting nightmare for you.' %years
    elif years <= 10:
        return 'Aww hell yeah, you only have %d more years to go buddy. It\'s almost over!' %years

def sendSergalFact():
    '''Returns a random sergal fact.'''
    return sergalFacts[random.randint(0, len(sergalFacts) - 1)]

def checkIfMemeDirExists():
    '''checks if ./memes exists. If it does, tacit returns. If it doesn't, it creates the directory'''
    if os.path.exists('./memes'):
        return
    else:
        os.mkdir('./memes')
        print('memes directory does not exist, creating...')

def sendMeme():
    '''Check to make sure meme directory exists, and create it if it doesn't. If it does exist but no images are in it, send the appropriate message. If images are present, return the path of a randomly selected one.'''
    if os.path.exists('./memes') and len(os.listdir('./memes')) != 0:
        files = os.listdir('./memes')
        return './memes/' + files[random.randint(0, len(files) - 1)]
    elif os.path.exists('./memes'):
        print('sendMeme() was called, but no memes are in ./memes')
        return 'no memes'
    else:
        checkIfMemeDirExists()
        return sendMeme()

async def downloadImage(URLs, filenames):
    """downloads images in jpg, png, and gif format\n
    URLS: list of URLs to images\n
    filenames: list of filenames that correspond to URLs"""
    checkIfMemeDirExists()
    for url in URLs:
        fileType = url.split('.')[-1]
        if bool(acceptableFileTypes.search(fileType)):
            if os.path.exists('./memes/%s' %filenames[URLs.index(url)]):
                return 2
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    with open("./memes/" + filenames[URLs.index(url)], "wb") as image:
                        image.write(await response.read())
                        print(filenames[URLs.index(url)], "added to memes")
    return 0

def fullwidth(text):
    '''converts a regular string to Unicode Fullwidth
    Preconditions: text, a string'''
    translator = ''
    translator = translator.maketrans('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~' , '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～')
    return text.translate(translator)