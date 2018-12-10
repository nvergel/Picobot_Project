
# CS5 Final Project
# Filename: milestone.py
# Names: Ignacio Lista Rosales, Shaurya Pednekar and Nicolás Pérez-Vergel
# Project: In this project we will write a Python program that writes Picobot programs. This piece of software will assess the "fitness" of each Picobot 
#          program to automatically evolve better and better Picobot programs using a biologically-inspired technique called "Genetic Algorithms".
# Starting date: 12/5/2018


import random


# Magic numbers and other useful variables:

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5
PATTERN = ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx"]
POSSIBLE_MOVES = ["N", "S", "E", "W"]
 
# Program class:

class Program:
    """A class that represents a single Picobot program
    """
    def __init__(self):
        """Constructs objects of type Program, setting self.rules to be an empty dictionary
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
        for x in range(NUMSTATES):
            for y in PATTERN:
                movedir = random.choice(POSSIBLE_MOVES)
                while movedir in y:
                    movedir = random.choice(POSSIBLE_MOVES)
                newstate = random.choice(range(NUMSTATES))
                self.rules[(x, y)] = (movedir, newstate)
        
    def getMove(self, state, surroundings):
        """This method accepts an integer state and a surroundings and returns a tuple containing the next move and the new state
        """
        return self.rules[(state, surroundings)]
    
    def mutate(self):
        """
        """
        state = random.choice(self.rules.keys())
        newdir = random.choice(POSSIBLE_MOVES)
        while newdir in state[1]:
            newdir = random.choice(POSSIBLE_MOVES)
        self.rules[state] = (newdir, random.choice(range(NUMSTATES)))
        
    def crossover(self, other):
        """
        """
        new = Program()
        num = random.choice(range(NUMSTATES-1))
        p1 = {x: self.rules[x] for x in self.rules if x[0] <= num}
        p2 = {x: other.rules[x] for x in other.rules if x[0] > num}	
        for x in p2:
            p1[x] = p2[x]
        new.rules = p1
        return new

        

# World class:
        
class World:
    """A class that simulates a Picobot environment
    """
    def __init__(self, initial_row, initial_col, program):
        """Constructs objects of type World
        """
        self.prow = initial_row
        self.pcol = initial_col
        self.state = 0
        self.prog = program
        self.room = [[' ']* WIDTH for row in range(HEIGHT)]

        for col in range(WIDTH):
              self.room[0][col] = "-"
              self.room[WIDTH-1][col] = "-"
        for row in range(HEIGHT):
              self.room[row][0] = "|"
              self.room[row][HEIGHT -1] = "|"
        self.room[0][0] = "+"
        self.room[0][WIDTH-1] = "+"
        self.room[HEIGHT-1][0] = "+"
        self.room[HEIGHT-1][WIDTH-1] = "+"

        self.room[initial_row][initial_col] = "P"
    
    def __repr__(self):
        """This method returns a string representation of the Picobot world
        """
        s = ""
        for row in range(HEIGHT):
            for col in range(0, WIDTH):
                s += self.room[row][col]
            s += "\n"
        return s
    
    def getCurrentSurroundings(self):
        """
        """
        s = ""
        if self.room[self.prow-1][self.pcol] == "-":
            s += "N"
        else: s += "x"

        if self.room[self.prow][self.pcol+1] == "|":
            s += "E"
        else: s += "x"
        
        if self.room[self.prow][self.pcol-1] == "|":
            s += "W"
        else: s += "x"
        
        if self.room[self.prow+1][self.pcol] == "-":
            s += "S"
        else: s += "x"
        
        return s
    
    def step(self):
        """
        """
        surr = self.getCurrentSurroundings()
		nextMove = self.prog.getMove(self.state, surr)
		self.state = nextMove[1]
		

