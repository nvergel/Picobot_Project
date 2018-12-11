# CS5 Final Project
# Filename: final.py
# Names: Ignacio Lista Rosales, Shaurya Pednekar and Nicolás Pérez-Vergel
# Project: In this project we will write a Python program that writes Picobot programs. This piece of software will assess the "fitness" of each Picobot 
#          program to automatically evolve better and better Picobot programs using a biologically-inspired technique called "Genetic Algorithms".
# Starting date: 12/10/2018


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
        """This method accepts an integer state and a surrounding (in the form of a list) and returns a tuple containing
           the next move and the new state
        """
        return self.rules[(state, surroundings)]
    
    def mutate(self):
        """This method chooses a single rule from self.rules and changes its value (the move and new state). This choice is random
           from within one of the valid moves.
        """
        state = random.choice(self.rules.keys())
        newdir = random.choice(POSSIBLE_MOVES)
        while newdir in state[1]:
            newdir = random.choice(POSSIBLE_MOVES)
        self.rules[state] = (newdir, random.choice(range(NUMSTATES)))
        
    def crossover(self, other):
        """This method accepts an object other of type Program and returns a new "offspring" of type Program containing some of the rules
           from self and the rest from other
        """
        new = Program()
        num = random.choice(range(NUMSTATES-1))
        p1 = {x: self.rules[x] for x in self.rules if x[0] <= num}
        p2 = {x: other.rules[x] for x in other.rules if x[0] > num}	
        for x in p2:
            p1[x] = p2[x]
        new.rules = p1
        return new

    def __gt__(self, other):
        """Redefinition of the greater than operator for the Program class
        """
        return random.choice([True, False])

    def __lt__(self, other):
        """Redefinition of the less than operator for the Program class
        """
        return random.choice([True, False])


# World class:
        
class World:
    """A class that simulates a Picobot environment
    """
    def __init__(self, initial_row, initial_col, program):
        """Constructs objects of type World
        """
        program.randomize()

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

        self.counter = 1
    
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
        """This method creates a string representing Picobot's surroundings at a given time
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
        """This method moves Picobot one step, updating sel.room and the state, row, and column of Picobot. It does not
           return anything
        """
        surr = self.getCurrentSurroundings()
        nextMove = self.prog.getMove(self.state, surr)
        self.state = nextMove[1]
        self.room[self.prow][self.pcol] = "o"

        if nextMove[0] == 'W':
            self.pcol -= 1
        if nextMove[0] == 'E':
            self.pcol += 1
        if nextMove[0] == 'N':
            self.prow -= 1
        if nextMove[0] == 'S':
            self.prow += 1
        
        if self.room[self.prow][self.pcol] == " ":
            self.counter += 1
        self.room[self.prow][self.pcol] = "P"
    
    def run(self, steps):
        """This method accepts a integer representing the number of steps to move
        """
        for i in range(steps):
            self.step()

    def fractionVisitedCells(self):
        """This method returns the floating-point fraction of cells in self.room that have been visited by Picobot. This is the 
           basic fitness score for a Picobot program
        """
        return self.counter/(HEIGHT-2)/(WIDTH-2)


# Other functions

def createPrograms(size):
    """
    """
    L = []
    for i in range(size):
        p = Program()
        p.randomize()
        L += [p]
    return L

def evaluateFitness(program, trials, steps):
    """
    """
    L = []
    for i in range(trials):
        w = World(random.choice(range(1,HEIGHT-1)), random.choice(range(1,WIDTH-1)), program)
        w.run(steps)
        L += [w.fractionVisitedCells()]
    return sum(L)/len(L)

def GA(popsize, numgens):
    """
    """

    