import sys
import copy
from superTicTacConsole import * 

# state of game with all the needed information to progress
class GameNode:
    # nodes can be constructed using a gameState, a move history
    def __init__(self, board, history, winArray):
        self.boardState = board
        self.moveHistory = history
        self.winArray = winArray
        self.validMoves = []  
        self.winState = 0

        self.checkForWin()
        self.listValidMoves()

    def makeMove(self, move):
        if move not in self.validMoves : 
            raise Exception("invalid move supplied")
        self.moveHistory.append(move)
        if len(self.moveHistory) % 2 == 0 or (len(self.moveHistory) == 0):
            self.boardState[move[0]][move[1]] = 2
        else:
            self.boardState[move[0]][move[1]] = 1  
        self.checkForWin()
        self.listValidMoves()

    # will detect if the last played board zone contains a win
    # it then projects those wins to a normal ticTacToe board
    # exploit the +1 +2 +3 feature of a small board section
    # horizontile relationship [a,b], [a+1,b], [a+2,b]
    # vertical relationship [a, b], [a, b+1], [a, b+2]
    # diagonal relationship [a,b], [a+1,b+1], [a+1,b+1] also works with minus
    # win array can be visualized as
        # [0,0,0],
        # [0,0,0],
        # [0,0,0]
    def updateWinArray(self):
        if self.moveHistory != [] : 
            # zone for the 3 by 3 board
            # we are only going to evaluate a win condition on the zone last played 
            # there's no reason to waste time checking every zone
            zone = projectCoordinateToBoardZone(self.moveHistory[-1])

            # these are the start coordinates for our 9 by 9 board
            # always the top left corner of a zone
            x0 = zone[0] * 3
            y0 =  zone[1] * 3

            for i in range(3) :    
                # horizontal check
                if self.boardState[x0][y0 + i] == self.boardState[x0 + 1][y0 + i] == self.boardState[x0 + 2][y0 + i] != 0:
                    self.winArray[zone[0]][zone[1]] = self.boardState[x0 + i][y0]
                    return
                # vertical check
                if self.boardState[x0 + i][y0] == self.boardState[x0 + i][y0 + 1] == self.boardState[x0 + i][y0 + 2] != 0:
                    self.winArray[zone[0]][zone[1]] = self.boardState[x0 + i][y0]
                    return

            # forward diagnonal
            if self.boardState[x0][y0] == self.boardState[x0 + 1][y0 + 1] == self.boardState[x0 + 2][y0 + 2] != 0: 
                self.winArray[zone[0]][zone[1]] = self.boardState[x0][y0]
                return

            # back diagonal
            if self.boardState[x0 + 2][y0] == self.boardState[x0 + 1][y0 + 1] == self.boardState[x0][y0 + 2] != 0: 
                self.winArray[zone[0]][zone[1]] = self.boardState[x0 + 2][y0]
                return
    
    # using the win array board, we check to see if there are any big board wins
    def checkForWin(self):
        self.updateWinArray()
        win = self.winArray
        for i in range(3):
            if win[i][0] == win[i][1] == win[i][2] != 0:         # check the three horizontiles
                self.winState = win[i][0]
                return                                           # simply returns the player number for the win
            if win[0][i] == win[1][i] == win[2][i] != 0:         # check the three verticals 
                 self.winState = win[0][i]
                 return
        if win[0][0] == win[1][1] == win[2][2] != 0:            # check for each diagonal
             self.winState = win[1][1]
             return
        if win[2][0] == win[1][1] == win[0][2] != 0:
             self.winState = win[1][1]
             return

    # will list all valid moves given a board state and a history
    # moves are listed as [y, x]
    def listValidMoves(self):
        self.validMoves = []
        # if the game is won then return no valid moves
        if len(self.moveHistory) > 0:
            bigBoard = projectCoordinateToNextBoardZone(self.moveHistory[-1])
            bb0 = bigBoard[0]
            bb1 = bigBoard[1]
            # if the return board has already been won by either 1 or 2
            if self.winArray[bb0][bb1] == 1 or self.winArray[bb0][bb1] == 2:
                self.validateAllPossible()
            # if we weren't sent back to an invalid board, select all tiles from that board
            else:
                for i in range(3):
                    for j in range(3):
                        move = []
                        move.append(3 * bigBoard[0] + i)
                        move.append(3 * bigBoard[1] + j)
                        if move not in self.moveHistory:
                            self.validMoves.append(move)
        else:
             self.validateAllPossible()


    # usually called when sent to an invalid square or at the start of a game
    # validates any coordinate that hasn't been played on a valid board zone
    def validateAllPossible(self):
        self.validMoves = []     
        for i in range(9):
            for j in range(9):
                # make all tiles playable
                move = [i,j]
                # except tiles that fall in the win zone, which is any big board win, mapped to all its smaller coordinates
                moveBB = projectCoordinateToBoardZone(move)
                moveBB0 = moveBB[0]
                moveBB1 = moveBB[1]
                # so 01 bigBoard is 00. if win[0][0] is 0, make a play
                if self.winArray[moveBB0][moveBB1] == 0 and move not in self.moveHistory:
                    self.validMoves.append(move)

# every move will effect the next move by projecting to a different board zone
# this takes a move and finds the next zone to be played
def projectCoordinateToNextBoardZone(move):
    output = []
    for x in move:
        if x == 0 or x == 3 or x == 6:
            output.append(0)
        if x == 1 or x == 4 or x == 7:
            output.append(1)
        if x == 2 or x == 5 or x == 8:
            output.append(2)
    # returns a point on the big board such as 2,2, which would be the right hand corner
    return output


# similar to the previous function, this one just finds which zone the move
# was played in, rather than projecting the next move
# output will be a coordinate like [1,2] symbolizing which board we played on
def projectCoordinateToBoardZone(move):
    output = []
    for x in move:
        if 0 <= x < 3:
            output.append(0)
        if 3 <= x < 6:
            output.append(1)
        if 6 <= x < 9:
            output.append(2)
    return output
