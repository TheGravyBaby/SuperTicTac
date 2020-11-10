# SuperTicTac

Super Tic Tac Toe is a much more complex game than the orignial. Like regular Tic Tac Toe (abbreviated TTT), Super Tic Tac Toe (STTT) has players attempting to
win three squares in a row on a game board. However, each of the squares themselves are a TTT board, and to win said square you must win TTT on the square's board. The final
caviate is that that whatever move was last played dictates the viable moves that are allowed for the next move. Wikipedia explains better than I do : 

  	"The game starts with X playing wherever they want in any of the 81 empty spots. This move "sends" their opponent to its relative location. For example, if X played in 
  	the top right square of their local board, then O needs to play next in the local board at the top right of the global board. O can then play in any one of the 
  	nine available spots in that local board, each move sending X to a different local board."

This program will not only allow two players to play against eachother, but you can also play against an AI. My AI uses a Monte Carlo Tree Search algorithm to approximate the best
move in any given position. There are few know heuristics for evaluating positions in the game, so MCTS is a very good method for a game with as many possibilities as STTT. 
Simply give it a search time and it will simulate as many games as it can in that time. Upon each move, the algorithm will actually save and reuse
relevant parts of the tree to improve efficiency. 

Currently this app is single threaded, though I am looking into the best multithreaded methods. On a Ryzen 1600 processor running on PyPy it is rather difficult to beat around 30 seconds of search time. Given a minute of search time, I am not able to beat it at all. 
