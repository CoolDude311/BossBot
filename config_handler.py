#!/usr/bin/env python3
"""Store settings in a TOML file"""

import os
import stat
import sys
import toml

config_path = "config.toml"

def checkConfig():
    """Checks to see if config file is properly configured and opens it. If not properly configured, returns an error (-1, improper permissions) or creates the file (file doesn't exist)"""
    if os.path.exists(config_path) and stat.filemode(os.stat(config_path)[0])[:3] == "-rw":
        return openConfig()
    elif os.path.exists(config_path):
        sys.exit("Config error: You do not have permission to read/write the config file.")
    else:
        return createConfig()

def openConfig():
    """Opens config_path and returns the resulting dictionary"""
    try:
        config = toml.load(config_path)
    except:
        sys.exit("Config error: There was an error parsing the configuration file at %s. It may have become corrupted. Please inspect it, or to delete it and run the bot again to create a new config file.")

    if len(config.keys()) == 0: #if user quit while setting up bot
        config = createConfig()

    verifyConfig(config)
    return config

def verifyConfig(config):
    """Checks the configuration file and makes sure all properties entered are proper\n
        config: a dictionary containing necessary configuration properties"""
    
    if "api_keys" in config.keys():
        if "discord" in config["api_keys"].keys() and config["api_keys"]["discord"] == "":
            sys.exit("Invalid config file: Discord API key")

def saveConfig(config):
    """Saves a dictionary as a toml configuration file at config_path. Returns an error if the file could not be saved\n
        config: a dictionary containing necessary configuration properties"""
    try:
        with open(config_path, "w") as f:
            toml.dump(config, f)
    except:
        print("Error writing config file. Make sure you have permission to write to the folder you're running the bot in.")
        return -1

def createConfig():
    """Gathers necessary information from the user and arranges it into a configuration dictionary"""
    config = {"api_keys":{}}

    config["api_keys"]["discord"] = input("Hi! It seems like this is your first time running me. Go ahead and paste your Discord API key: ")

    saveConfig(config)
    return config