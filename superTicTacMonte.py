import os
import sys
from superTicTacNodes import *
from superTicTacConsole import *
import math as m 
import random

global_playouts = 0
# the bigger this number, the more games the tree will search through
allowed_playouts = 320

class monteNode(): 
    def __init__(self, GameNode, Parent):
        self.GameNode = GameNode
        self.Parent = Parent
        self.Children = []
        self.ChildPlayouts = 0
        self.WonPlayouts = 0
        self.UCB1 = m.inf
        
    def calculateUCB1(self):
        self.UCB1 = self.WonPlayouts / self.ChildPlayouts + m.pow(2, .5) * m.pow(m.log(self.Parent.ChildPlayouts) / self.ChildPlayouts, .5)
        # after a won playout compute UBC
        # self.Parent.ChildPlayouts
 
    
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
        global_playouts += 1
        node.ChildPlayouts += 1    
        backpropogate_node(node, 0)
    
    # check for wins     
    elif node.GameNode.winState != 0 :
        global_playouts += 1
        node.ChildPlayouts += 1
        backpropogate_node(node, node.GameNode.winState)

    else : 
        # sort by UCB1 order, gotta figure out how to sort here,
        node.Children = sorted(node.Children, key=lambda  child: child.UCB1)
        # print(node.Children) 
        
        random.seed(a=None, version=2)
        num = random.randint(0, len(node.Children)) - 1

        # printGameState(node.Children[num].GameNode)
        # print("Expanding...")
        
        node.ChildPlayouts += 1
        monte_expand(node.Children[num])


def backpropogate_node(node, winloss):
    
    # nodes for player two need to propogate with wins losses for 2    
    if len(node.GameNode.moveHistory) % 2 == 0 :
        if winloss == 2 : 
            node.WonPlayouts += 1
    
    elif len(node.GameNode.moveHistory) % 2 != 0 :
        if winloss == 1 : 
            node.WonPlayouts += 1

    elif winloss == 0 : 
        node.WonPlayouts += .5
 
    # non root node 
    if node.Parent != None :
        node.calculateUCB1()
        backpropogate_node(node.Parent, winloss)
    
    # root node
    else :
        print("I've simulated {} games out of {}.".format(global_playouts, allowed_playouts), end="\r", flush=True)



def monte_runner(gameNode):
    global global_playouts
    tree_root = monteNode(gameNode, None)

    print("Simulating games...")
    # unless a child has a won game, if so just go to that one! 
    while global_playouts <  allowed_playouts :
        monte_expand(tree_root)
    
    # pick the node with the highest ubc1
    tree_root.Children = sorted(tree_root.Children, key=lambda child: child.ChildPlayouts)
    best_move = tree_root.Children[-1].GameNode.moveHistory[-1]

    # print("My favorite move is {} with {} percent wins".format(coordinates_to_display(best_move), tree_root.Children[-1].WonPlayouts / global_playouts * 100))
    # print("Its UBC1 score is {}".format(tree_root.Children[-1].UCB1))
    # print("The second best UCB1 score is {}".format(tree_root.Children[-2].UCB1))
    # input()
    global_playouts = 0

    return best_move

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y
