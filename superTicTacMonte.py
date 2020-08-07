import os
import sys
from superTicTacNodes import *
import math as m 
import random

# determines the number of playouts the algorithm will attempt before making a descision
playouts = 100

class monteNode(): 
    def __init__(self, GameNode, Parent, ParentPlayouts):
        self.GameNode = GameNode
        self.Parent = Parent
        self.Children = []
        self.ParentPlayouts = ParentPlayouts
        self.ChildPlayouts = 0
        self.WonPlayouts = 0
        self.UCB1 = m.inf
        
    def calculateUCB1(self):
        self.UCB1 = self.WonPlayouts / self.ChildPlayouts + m.pow(2, .5) * m.pow(m.log(self.ParentPlayouts) , .5)
        # after a won playout compute UBC
 
# 1. Create the root monte node... (could be a root or any node really)
def monte_initiate(GameNode):
    return monteNode(GameNode, None, 0)
    
# 2. EXPAND!  For valid moves in that game node, make child nodes           
def monte_expand(MonteNode):
    
     # only need to expand if we haven't already
     if len(MonteNode.Children) == 0 : 
        # make new child nodes
        for move in MonteNode.GameNode.validMoves : 
            newGameState = makeMoveNewBoard(MonteNode.GameNode.boardState, move)
            MonteNode.Children.Add(monteNode(newGameState, MonteNode, MonteNode.ParentPlayouts))
    monte_select(MonteNode)


# 3. SELECT! Pick a node to keep traveling down
def monte_select(MonteNode):
    
    # check for draws on this node
    if MonteNode.GameNode.boardState.winState == 0 and len(MonteNode.GameNode.boardState.validMoves) == 0 :
        print("Found a draw")
    
    # check for wins     
    elif MonteNode.GameNode.boardState.winState != 0 :
        print("Found a win")

    # sort by UBC1 order, gotta figure out how to sort here,
        
    
    # if no ubc1 advantage, pick a random number, get that child, and then run the expansion
    else :
        randomNum = random.randint(0, len(MonteNode.GameNode.validMoves))   
        monte_expand(MonteNode.Children[randomNum])
    



# 4. Repeat 2, for all the valid moves make child nodes 

def backpropogate_node(MonteNode):
    print("Backpropogate")
    