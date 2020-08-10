import os
import sys
from superTicTacNodes import *
from superTicTacConsole import *
import math as m 
import random

# determines the number of playouts the algorithm will attempt before making a descision

player = 1
global_playouts = 0
allowed_playouts = 100

class monteNode(): 
    def __init__(self, GameNode, Parent):
        self.GameNode = GameNode
        self.Parent = Parent
        self.Children = []
        self.ChildPlayouts = 0
        self.WonPlayouts = 0
        self.UCB1 = m.inf
        
    def calculateUCB1(self):
        self.UCB1 = self.WonPlayouts / self.ChildPlayouts + m.pow(2, .5) * m.pow(m.log(global_playouts) / self.ChildPlayouts, .5)
        # after a won playout compute UBC
 
# 1. Create the root monte node... (could be a root or any node really)
def monte_initiate(GameNode):   
    root_node =  monteNode(GameNode, None)
    monte_expand(root_node)

    
# 2. EXPAND!  For valid moves in that game node, make child nodes           
def monte_expand(node):
    
     # only need to expand if we haven't already
    if len(node.Children) == 0 : 
        # make new child nodes
        for move in node.GameNode.validMoves : 
           # newGameState = makeMoveNewBoard(node.GameNode, move)
            node.Children.append(monteNode(makeMoveNewBoard(node.GameNode, move), node))       
    monte_select(node)


# 3. SELECT! Pick a node to keep traveling down
def monte_select(node):

    global global_playouts
    
    # check for draws on this node
    if node.GameNode.winState == 0 and len(node.GameNode.validMoves) == 0 :
        printGameState(node.GameNode)
        global_playouts += 1
        print("Found a draw")    
        backpropogate_node(node, 0)
    
    # check for wins     
    elif node.GameNode.winState != 0 :
        printGameState(node.GameNode)
        global_playouts += 1
        print("Found a win")
        if node.GameNode.winState == player :
            backpropogate_node(node, 1)
        else : 
             backpropogate_node(node, -1)


    else : 
        # sort by UCB1 order, gotta figure out how to sort here,
        # node.Children = sorted(node.Children, key=lambda  child: child.UCB1)
        # print(node.Children) 
        
        random.seed(a=None, version=2)
        num = random.randint(0, len(node.Children)) - 1

        printGameState(node.Children[num].GameNode)
        print("Expanding...")

        # input()
        monte_expand(node.Children[num])

    

# 4. Repeat 2, for all the valid moves make child nodes 

def backpropogate_node(node, winloss):
    # global global_playouts

    node.WonPlayouts += winloss
    node.ChildPlayouts += 1
    node.calculateUCB1()

    # this would be the root node 
    if node.Parent != None :
        backpropogate_node(node.Parent, winloss)
    else :
        print("Got back to the root")
        if global_playouts < allowed_playouts :
            monte_select(node)



def runAMonte():
    initial_board = [ [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    initial_history = []
    game = GameNode(initial_board, initial_history)
    monte_initiate(game)

runAMonte()