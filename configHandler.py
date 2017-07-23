#!/usr/bin/env python3
'''This module handles the config file that hosts API keys, commands, and users.'''
import os
import stat
import sys

def checkConfig():
    '''Checks to see if config directory exists, and if the user has necesary permissions to read and write to the files. If the user does not have permission, it exits with an error message. If the files do not exist, it will automatically set them up. If possible, returns openConfig()'''
    if os.path.exists('./config/main.conf') and stat.filemode(os.stat('./config/main.conf')[0])[:3] == '-rw':
        return openConfig()
    elif os.path.exists('./config/main.conf'):
        sys.exit('Config error: You do not have permission to read/write the config file.')
    else:
        makeConfig()

def openConfig():
    '''Opens the existing "./config/main.conf" file in the root directory, and returns a list containing its lines.'''
    #TODO: Check to make sure main.conf is valid
    inFilePipe = open('./config/main.conf', 'r')
    output = inFilePipe.readlines()
    inFilePipe.close()
    print('The configuration file was successfully opened!')
    return output

def makeConfig():
    '''Creates the config directory "./config" in the root directory, and creates configuration files.'''
    os.mkdir('./config')
    outFilePipe = open('./config/main.conf', 'w')
    apiKey = input('Hi! Seems like this is your first time running me. Let\'s go ahead and set up your API keys. Go ahead and enter your Discord API key: ')
    outFilePipe.write('Discord API Key:%s\n' %apiKey)
    outFilePipe.close()

def makeServerDir():
    '''Creates the directory to store configurations for individual servers after checking to make sure it does not already exist.'''
    if os.path.exists('./config/servers'):
        return
    else:
        os.mkdir('./config/servers')

def createServerConfig(serverID):
    '''Preconditions: the valid ID of a Discord server.
Creates a new configuration file for serverID after checking to make sure it doesn't already exist.'''
    if os.path.exists('./config/servers/%s.conf' %serverID):
        print('Tried to make a config file for server %s, but an error occured. Either it already exists, or you don\'t have permission to write to the servers directory in config. Try checking your permissions.' %serverID)
    else:
        makeServerDir()
        outFilePipe = open('./config/servers/%s.conf' %serverID, 'w')
        outFilePipe.write('Server ID:\t%s\n' %serverID)
        outFilePipe.close()

def readApiKeys():
    '''Reads the API keys in main.conf, and returns a list of the keys only and not their designation.'''
    keys = checkConfig()
    splitKeys = []
    for key in keys:
        splitKeys.append(key.split(':')[1])
    return splitKeys

readApiKeys()