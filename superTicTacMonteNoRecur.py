import os
import sys
from superTicTacNodes import *
from superTicTacConsole import *
import math as m 
import random
import time

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
        self.UCB1 = self.WonPlayouts / self.Visits + m.pow(((2 * m.log(self.Parent.Visits)) / self.Visits), .5)
 
    
# SELECT! Pick a node to keep traveling down
def monte_select(node):
    
    # if we have no children to visit, we'll have to make some
    if len(node.Children) == 0 :
        node.Visits += 1
        return node
    
    # if we do have children to visit, sort and pick highest ucb1
    else :
        node.Children.sort(key=lambda  child: child.UCB1)              
        node.Children[-1].Visits += 1
        if node.Parent == None : 
            node.Visits += 1
        return node.Children[-1]
    
# EXPAND!  For valid moves in that game node, make child nodes           
def monte_expand(node):
    if len(node.Children) < len(node.GameNode.validMoves) : 
        # make new child nodes
        for move in node.GameNode.validMoves : 
            node.Children.append(monteNode(makeMoveNewBoard(node.GameNode, move), node))       
    return node

def monte_select_single(node):
    # if we have no children to visit, we'll have to make some
    # pass the node on
    if node.Children == 0 :
        node.Visits += 1
        return node
    
    # if we do have children to visit!
    else :
        # did we visit these kids before?
        # if so pass on for expansion 
        if node.Visits >= len(node.Children) :
            return node
        
        # we have a kid we haven't visited
        else :
            node.Children.sort(key=lambda  child: child.UCB1)              
            node.Children[-1].Visits += 1
            # if we are leaving the root node, remember to give it a visit 
            # we will only give root node a visit upon departure
            if node.Parent == None : 
                node.Visits += 1
            return node.Children[-1]
    


# this expands a single node, saves memory
def monte_expand_single(node):
    
    # UCB for unexplored nodes is inf, so always make a new one if we have the option
    if len(node.Children) < len(node.GameNode.validMoves) : 
        # make new child node
        made_moves = []
           
        for child_node in node.Children :
            made_moves += child_node.GameNode.moveHistory[-1]
             
        for move in node.GameNode.validMoves :
            if move not in made_moves :
                node.Children.append(monteNode(makeMoveNewBoard(node.GameNode, move), node))    
                break               
   
    return node


def backpropogate_node(node, winloss):
    
    # last move was player 2
    if len(node.GameNode.moveHistory) % 2 == 0 :
        if winloss == 2 : 
            node.WonPlayouts += 1
        elif winloss == 1 : 
            node.WonPlayouts -= 1
    
    # last move was player 1
    elif len(node.GameNode.moveHistory) % 2 == 1 :
        if winloss == 1 : 
            node.WonPlayouts += 1
        elif winloss == 2 : 
            node.WonPlayouts -= 1

    node.calculateUCB1()
    # if we haven't reached the root of the tree, return the parent so we can keep recursing
    if node.Parent != None :
        return node.Parent
    
    # we actually shouldn't hit this as we won't call if there is a parent
    # but why not put it here, costs nothing and prevents an error...
    else : 
        return node


# using a global tree root will allow us to re use the tree. this will be a huge efficiency improvement
def monte_runner(gameNode, allocated_time):
    global global_playouts
    global last_selected_node
    tree_root = None
    # reusedData = False
    
    # if this is our first move, just make a tree
    if last_selected_node == None :
        tree_root = monteNode(gameNode, None)
    
    # if not, we should try to re use data from previous searches
    # as of now this function will not allow monte to play itself 
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
    start_time = time.time()

    search_locked = True
    while search_locked :
              
        tree_root = monte_select(tree_root)
              
        # if draw back propogate a draw
        if len(tree_root.GameNode.validMoves) == 0 and tree_root.GameNode.winState == 0 :
            printGameState(tree_root.GameNode)
            global_playouts += 1
            tree_root.Visits += 1
            while tree_root.Parent != None :     
                tree_root = backpropogate_node(tree_root, 0)
            if time.time() - start_time > allocated_time :
                search_locked = False
        
        # if win backprop a win    
        elif tree_root.GameNode.winState != 0 :
            winner = tree_root.GameNode.winState
            printGameState(tree_root.GameNode)
            global_playouts += 1
            tree_root.Visits += 1
            while tree_root.Parent != None :    
                tree_root = backpropogate_node(tree_root, winner)
            if time.time() - start_time > allocated_time :
                search_locked = False
        
        else :
            tree_root = monte_expand(tree_root)

        
    # by end of that above loop, we should be back with root node
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

    # total_time = time.time() - start_time
    # print("Tree search took {} seconds to run {} simulations.".format(total_time, global_playouts))
    # input()
    
    global_playouts = 0  
    return best_move