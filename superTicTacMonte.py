from superTicTacNodes import *
from superTicTacConsole import *
import math as m 
import random
import time
import numpy as np

global_playouts = 0
last_selected_monteNode = None
global_expand_times = []
global_backPropogate_times = []

class MonteNode(): 
    def __init__(self, gameNode, Parent):
        self.gameNode = gameNode
        self.parent = Parent
        self.children = []
        self.visits = 0
        self.wonPlayouts = 0
        self.ucb1 = m.inf
        self.lock = 0
        self.simulatedMoves = []
        
    def calculateUCB1(self):
        self.ucb1 = self.wonPlayouts / self.visits + m.pow(((2 * m.log(self.parent.visits)) / self.visits), .5)
 

def monte_runner(gameNode, allocated_time) : 
    tree_root = MonteNode(gameNode, None)

    print("Simulating games...")
    start_time = time.time()
    search_locked = True

    while search_locked :
        # printGameState(tree_root.gameNode)
        # print("Top of search")
        selectedNode = selection(tree_root)
        # printGameState(selectedNode.gameNode)
        # print("Node for selection")

        # we don't want to simulate games if there is a win available
        # rather than expanding a node, just backpropogate the node with the winning child 
        selectedNodeHasWin = None
        for child in selectedNode.children :
            if child.gameNode.winState != 0 :
                selectedNodeHasWin = child
                break
        if selectedNodeHasWin != None :
             selectedNodeHasWin.visits += 1
             tree_root = backpropogate(selectedNodeHasWin, selectedNodeHasWin.gameNode.winState)
        else : 
            expandedNode = expansion(selectedNode)
            # printGameState(expandedNode.gameNode)
            # print("Expanded node")
            completedGame = simulation(expandedNode)
            # printGameState(completedGame.gameNode)
            # print("Completed Game")

        tree_root = backpropogate(completedGame, completedGame.gameNode.winState)

        if time.time() - start_time > allocated_time :
            search_locked = False

    # by end of that above loop, we should be back with root monteNode
    # pick the monteNode visited most, if UBC theory is correct this is best monteNode
    tree_root.children.sort(key=lambda child: child.visits)
    best_move = tree_root.children[-1].gameNode.moveHistory[-1]
    
    print("My favorite move is {} with {} wins and {} percent wins".format(coordinates_to_display(best_move), tree_root.children[-1].wonPlayouts, tree_root.children[-1].wonPlayouts / global_playouts * 100))
    print("Its UBC1 score is {}".format(tree_root.children[-1].ucb1))
    # print("Reused Tree Data: {}".format(reusedData))
    total_time = time.time() - start_time
    print("Tree search took {} seconds to run {} simulations with a rate of {} simulations per second".format(total_time, global_playouts, global_playouts / total_time))
    # print("Backprop average time is {}".format(statistics.mean(global_backPropogate_times)))
    # print("Expand average time is {}".format(statistics.mean(global_expand_times)))
    input()

    global_playouts = 0 

    return best_move

# select a monteNode without a win 
def selection(monteNode):
    monteNode.visits += 1
    # this monteNode has moves that have not been explored, return it for expansion
    if len(monteNode.children) <= len(monteNode.gameNode.validMoves) :
        return monteNode
    else : 
        # this monteNode has explored all possible moves, pick the one with the best ucb score
        return selection(monteNode.children[-1])

def expansion(monteNode):
    movesToExplore = copy.deepcopy(monteNode.gameNode.validMoves)
    # making randomized moves helps a lot with tree parallelization
    for move in monteNode.simulatedMoves :
        movesToExplore.remove(move)
    
    randomIndex = random.randint(0, len(movesToExplore) - 1)
    monteNode.simulatedMoves.append(movesToExplore[randomIndex])
    newgameNode = GameNode(copy.deepcopy(monteNode.gameNode.boardState), copy.deepcopy(monteNode.gameNode.moveHistory), copy.deepcopy(monteNode.gameNode.winArray))
    newgameNode.makeMove(movesToExplore[randomIndex])
    monteNode.children.append(MonteNode(newgameNode, monteNode))   

    return monteNode.children[-1]

def simulation(monteNode):
    # printGameState(monteNode.gameNode)
    # print("Simulating...")
    monteNode.visits += 1
    # if no valid moves (draw) or a win, this is the end of out simulation
    if len(monteNode.gameNode.validMoves) == 0  or monteNode.gameNode.winState != 0:
        return monteNode  
    # not the end of out simulation. expand the monteNode we're on and go deeper into the tree
    else:
        return simulation(expansion(monteNode))

def backpropogate(monteNode, winloss) :
    # last move was player 2
    if len(monteNode.gameNode.moveHistory) % 2 == 0 :
        if winloss == 2 : 
            monteNode.wonPlayouts += 1
        elif winloss == 1 : 
            monteNode.wonPlayouts -= 1

    # last move was player 1
    elif len(monteNode.gameNode.moveHistory) % 2 == 1 :
        if winloss == 1 : 
            monteNode.wonPlayouts += 1
        elif winloss == 2 : 
            monteNode.wonPlayouts -= 1
            
    monteNode.children.sort(key=lambda  child: child.ucb1)
    # if we haven't reached the root of the tree, sort the UBC1, return the parent so we can keep recursing 
    if monteNode.parent != None :
        monteNode.calculateUCB1()
        return backpropogate(monteNode.parent, winloss)
    # we have reached the top of the tree, no more recursion just return the monteNode 
    else : 
        return monteNode
