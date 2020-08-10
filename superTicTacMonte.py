import os
import sys
from superTicTacNodes import *
from superTicTacConsole import *
import math as m 
import random

# these should eventually be moved
player = 2
global_playouts = 0
# the bigger this number, the more games the tree will search through
allowed_playouts = 40

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
 
    
# EXPAND!  For valid moves in that game node, make child nodes           
def monte_expand(node):
    
    # only need to expand if we haven't already
    if len(node.Children) == 0 : 
        # make new child nodes
        for move in node.GameNode.validMoves : 
           # newGameState = makeMoveNewBoard(node.GameNode, move)
            node.Children.append(monteNode(makeMoveNewBoard(node.GameNode, move), node))       
    monte_select(node)


# SELECT! Pick a node to keep traveling down
def monte_select(node):

    global global_playouts
    
    # check for draws on this node
    if node.GameNode.winState == 0 and len(node.GameNode.validMoves) == 0 :
        # printGameState(node.GameNode)
        global_playouts += 1
        # print("Found a draw")    
        backpropogate_node(node, 0)
    
    # check for wins     
    elif node.GameNode.winState != 0 :
        # printGameState(node.GameNode)
        global_playouts += 1
        # print("Found a win")
        if node.GameNode.winState == player :
            backpropogate_node(node, 1)
        else : 
             backpropogate_node(node, -1)

    else : 
        # sort by UCB1 order, gotta figure out how to sort here,
        node.Children = sorted(node.Children, key=lambda  child: child.UCB1)
        # print(node.Children) 
        
        random.seed(a=None, version=2)
        num = random.randint(0, len(node.Children)) - 1

        # printGameState(node.Children[num].GameNode)
        # print("Expanding...")

        monte_expand(node.Children[num])


def backpropogate_node(node, winloss):
    node.WonPlayouts += winloss
    node.ChildPlayouts += 1
    node.calculateUCB1()

    # this would be the root node 
    if node.Parent != None :
        backpropogate_node(node.Parent, winloss)
    else :
        # clear()
        print("I've simulated {} games.".format(global_playouts), end="\r", flush=True)



def monte_runner(gameNode):
    global global_playouts
    tree_root = monteNode(gameNode, None)

    print("Simulating games...")
    while global_playouts <  allowed_playouts :
        monte_expand(tree_root)
    
    tree_root.Children = sorted(tree_root.Children, key=lambda child: safe_div(child.WonPlayouts, child.ChildPlayouts))
    best_move = tree_root.Children[-1].GameNode.moveHistory[-1]

    # clear()
    # print("I've completed {} games".format(global_playouts))
    # print("My favorite move is {}".format(coordinates_to_display(best_move)))
    global_playouts = 0

    return best_move

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y


# monte_runner()