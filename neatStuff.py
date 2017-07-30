#!/usr/bin/env python3
'''This module contains functions to be used as responses in main.py'''
import google
import os
import random
import urllib.request

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

def downloadMeme(URLs, filenames):
    '''checks to make sure the meme directory exists, and if it doesn't, creates the directory. If it does exist, downloads the images in URLs.
    Preconditions: URLs, a list containing valid URLs with images.
    filenames, a list containing filenames to match with the URLS.'''
    checkIfMemeDirExists()
    for url in URLs:
        print('URL: %s\nfilename: %s' %(url, filenames[URLs.index(url)]))
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})        
        openedRequest = urllib.request.urlopen(request)
        print('Downloading image %s...' %filenames[URLs.index(url)])
        image = open('./memes/%s' %filenames[URLs.index(url)], 'wb')
        image.write(openedRequest.read())
        image.close()
        print('%s downloaded and saved to ./memes' %filenames[URLs.index(url)])

def fullwidth(text):
    '''converts a regular string to Unicode Fullwidth
    Preconditions: text, a string'''
    translator = ''
    translator = translator.maketrans('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~' , '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～')
    return text.translate(translator)

def search(term):
    '''Search Google for term and return the first hit.
    Preconditions: term, a str to search Google for
    Postconditions: returns a list of matching URLs'''
    results = []
    print('Searching google for %s...' %term)
    for url in google.search(term, start=1, stop=2, num=1):
        print('Search result for %s: %s' %(term, url))
        results.append(url)
    return results

if __name__ == '__main__':
    search('sergals')