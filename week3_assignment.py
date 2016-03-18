"""
Created on Wed Mar  9 17:13:11 2016

@author: andrewscott
 
 
Mini-max Tic-Tac-Toe Player
"""
import poc_ttt_gui
import random
import math
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
try:
    import codeskulptor
    codeskulptor.set_timeout(60)
except ImportError as _error:
    print _error   


# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}
PLAYER = {2: "X", 3: "0"}
COUNT = 0
DEPTH = 0
BEST = float("-inf")

DEBUG_BOARDS = [[]]
DEBUG_MM = False
DEBUG_MS = False

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """ 
    best_score = float("-inf") * SCORES[player]
    best_move = (-1, -1)
    score = 0
    valid_moves = board.get_empty_squares()
    number_free_moves = len(valid_moves)
    winnable_number_moves = (board.get_dim()**2) - (2*board.get_dim()-1)
    moves_made = board.get_dim()**2 - number_free_moves
    boards = [board.clone() for dummy_idx in range(len(valid_moves))]
    for dummy_idx in range(len(valid_moves)):
        boards[dummy_idx].move(valid_moves[dummy_idx][0],
                              valid_moves[dummy_idx][1],
                              player)

    #if any board is at endgame, execute this block
    for dummy_idx in range(len(boards)):
        if boards[dummy_idx].check_win():
            score = SCORES[boards[dummy_idx].check_win()]
            if score == SCORES[player]:
                return score, valid_moves[dummy_idx]
       
    
    for dummy_idx in range(len(boards)):
        if boards[dummy_idx].check_win():
            score = SCORES[boards[dummy_idx].check_win()]
            if score * SCORES[player] > best_score * SCORES[player]:
                best_score = score
                best_move = valid_moves[dummy_idx]
                #end 'found end of game' block
        #non-endgame block
        else:
            next_i = mm_move(boards[dummy_idx], provided.switch_player(player))
            score = next_i[0]
            if score == SCORES[player]:
                return score, valid_moves[dummy_idx]
            elif score * SCORES[player] > best_score * SCORES[player]:
                best_score = score
                best_move = best_move = valid_moves[dummy_idx]
            #end of non-endgame block
    return best_score, best_move
             

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]


def rnd():
    """
    used to populate a TTT board with semi-random values.
    """
    a_number = random.randrange(10)
    #lets weight the odds
    if a_number < 2:
        return 2
    if a_number < 4:
        return 3
    return 1


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#dimension = 2
#board_contents = [[2, 1, 1], [3, 1, 1], [2, 3, 1]]
#board_contents = [[2, 2, 3], [3, 1, 1], [2, 3, 1]]
#board_contents = [[rnd(), rnd(), rnd()], [rnd(), rnd(), rnd()], [rnd(), rnd(), rnd()]]
#board_contents = [[rnd() for dummy_idx in range(dimension)] for dummy_idy in range(dimension)]
#board_contents = [[1 for dummy_idx in range(dimension)] for dummy_idy in range(dimension)]
#board_contents = [[1, 1], [3, 2]]

#great test case for optimization
#board_contents = provided.TTTBoard(3, False, [[2, 3, 2], [1, 3, 1] ,[2, 1, 1]])
#print move_wrapper(board_contents, provided.PLAYERO, 1)
#provided.play_game(move_wrapper, 1, False)

#print len(board_contents)
#for line in board_contents:
#    print line
#print board_contents
#my_board = provided.TTTBoard(len(board_contents), False, board_contents)
#print my_board
#print mm_move(my_board, 2)
#print "BEST", BEST
#print my_board._board


#for depth in range(len(DEBUG_BOARDS)):
#    print "Depth:", depth
#    for defs_not_a_board in (DEBUG_BOARDS[depth]):
        #for board_line in defs_not_a_board:
        #    print board_line
        #print "\n"