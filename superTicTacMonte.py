import os
import sys
from superTicTacNodes import *
from superTicTacConsole import *
import math as m 
import random

global_playouts = 0
last_selected_node = None

class monteNode(): 
    def __init__(self, GameNode, Parent):
        self.GameNode = GameNode
        self.Parent = Parent
        self.Children = []
        self.Visits = 0
        self.WonPlayouts = 0
        self.UCB1 = m.inf
        
    def calculateUCB1(self):
        self.UCB1 = self.WonPlayouts / self.Visits + m.pow(2 * m.log(self.Parent.Visits) / self.Visits, .5)
 
    
# EXPAND!  For valid moves in that game node, make child nodes           
def monte_expand(node):
    
    # only need to expand if we haven't already
    # this guy gets called a lot could be faster
    if len(node.Children) == 0 : 
        # make new child nodes
        for move in node.GameNode.validMoves : 
            node.Children.append(monteNode(makeMoveNewBoard(node.GameNode, move), node))       
    monte_select(node)


# SELECT! Pick a node to keep traveling down
def monte_select(node):
    
    global global_playouts
    
    # check for draws on this node
    if node.GameNode.winState == 0 and len(node.GameNode.validMoves) == 0 :
        global_playouts += 1
        node.Visits += 1    
        backpropogate_node(node, 0)
    
    # check for wins     
    elif node.GameNode.winState != 0 :
        global_playouts += 1
        node.Visits += 1
        backpropogate_node(node, node.GameNode.winState)

    else : 
        # sort by UCB1 order, select node with highest value
        node.Children.sort(key=lambda  child: child.UCB1)        
        node.Visits += 1
        monte_expand(node.Children[-1])


def backpropogate_node(node, winloss):
    
    # nodes for player two need to propogate with wins losses for 2    
    if len(node.GameNode.moveHistory) % 2 == 0 :
        if winloss == 2 : 
            node.WonPlayouts += 1
        elif winloss == 1 : 
            node.WonPlayouts -= 1
    
    elif len(node.GameNode.moveHistory) % 2 != 0 :
        if winloss == 1 : 
            node.WonPlayouts += 1
        elif winloss == 2 : 
            node.WonPlayouts -= 1

    # non root node 
    if node.Parent != None :
        node.calculateUCB1()
        backpropogate_node(node.Parent, winloss)
    
    # root node
    else :
        print("I've simulated {} games.".format(global_playouts), end="\r", flush=True)


# using a global tree root will allow us to re use the tree. this will be a huge efficiency improvement
def monte_runner(gameNode, allowed_playouts):
    global global_playouts
    global last_selected_node
    tree_root = None
    # reusedData = False
    
    # if this is our first move, just make a tree
    if last_selected_node == None :
        tree_root = monteNode(gameNode, None)
    
    # if not, we should try to re use data from previous searches
    else : 
        for child_node in last_selected_node.Children : 
            if gameNode.moveHistory == child_node.GameNode.moveHistory : 
                tree_root = child_node
                tree_root.Parent = None
                # reusedData = True
                break
      
        # there is a chance that we didn't simulate the move, though that is unlikely after many simulations'
        # even so, if the move hasn't been evaluated we'll need to make a new tree
        if tree_root == None : 
            tree_root = monteNode(gameNode, None)
    

    print("Simulating games...")
    # unless a child has a won game, if so just go to that one! 
    while global_playouts <  allowed_playouts :
        monte_expand(tree_root)
    
    # pick the node visited most, if UBC theory is correct this is best node
    tree_root.Children.sort(key=lambda child: child.Visits)
    best_move = tree_root.Children[-1].GameNode.moveHistory[-1]
    
    # to save the data, we pick the node we're making the move to and save that
    # this works if we assume the other player is a human and not updating the same tree
    # not good for algorithm self play
    last_selected_node = tree_root.Children[-1]

    # print("My favorite move is {} with {} percent wins".format(coordinates_to_display(best_move), tree_root.Children[-1].WonPlayouts / global_playouts * 100))
    # print("Its UBC1 score is {}".format(tree_root.Children[-1].UCB1))
    # print("Reused Tree Data: {}".format(reusedData))
    # input()
    global_playouts = 0

    return best_move