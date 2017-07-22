#!/usr/bin/env python3
'''This module contains functions to be used as responses in main.py'''
import random

def rollDice(dieSides=6):
    '''Preconditions: an integer (dieSides). Default is 6.
    Postconditions: returns an integer between 1 and dieSides.'''
    return random.randint(1, dieSides)
