# CS5 Final Project
# Filename: start.py
# Names: Ignacio Lista Rosales, Shaurya Pednekar and Nicolás Pérez-Vergel
# Project: 
# Starting date: 12/3/2018


import random


# Magic numbers:

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5


# Program class:

class Program:
    """A class that represents a single Picobot program
    """
    def __init__(self):
        """Construct objects of type Program, setting self.rules to be an empty dictionary
        """
        self.rules = {}

    def __repr__(self):
        """This method returns a string representation of the Picobot program in such a way that it can
           be pasted straight into the Picobot simulator
        """
        s = ""

        Keys = list(self.rules.keys()) 
        sortedKeys = sorted(Keys)

        for key in sortedKeys:
            s += str(key[0])+ " " + key[1] + " -> " + self.rules[key][0] + " " + str(self.rules[key][1]) + "\n"

        return s

    def randomize(self):
        """This method generates a random full set of Picobot rules for the program's self.rules dictionary,
           The set of rules is a combination of each Picobot state with all of the 9 possible surroundings
        """
        PATTERN = ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx"]
        POSSIBLE_MOVES = ["N", "S", "E", "W"]

        for x in range(NUMSTATES):
            for y in PATTERN:
                movedir = random.choice(POSSIBLE_MOVES)
                while movedir in y:
                    movedir = random.choice(POSSIBLE_MOVES)
                newstate = random.choice(range(NUMSTATES))
                self.rules[(x, y)] = (movedir, newstate)
    

# World class:
        
class World:
    """
    """
    def __init__(self):
        """
        """

    def __repr__(self):
        """
        """