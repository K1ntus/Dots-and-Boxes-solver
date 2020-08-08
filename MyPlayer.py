#############################
##CS4386 Semester B, 2019-2020
##Assignment 2
##Name: Jordane Masson
##Student ID: [40128550]
###########################
# #
# # Alpha-Beta Algorithm mostly inspired from here: 
# # https://github.com/K1ntus/Othello-Solver/blob/master/intelligence/movemanager/AlphaBeta.py
# # ( which is actually my code. At least for this part of the repository. )
# # 
###########################     
#   ____        _            _              _   ____                     
#  |  _ \  ___ | |_ ___     / \   _ __   __| | | __ )  _____  _____  ___ 
#  | | | |/ _ \| __/ __|   / _ \ | '_ \ / _` | |  _ \ / _ \ \/ / _ \/ __|
#  | |_| | (_) | |_\__ \  / ___ \| | | | (_| | | |_) | (_) >  <  __/\__ \
#  |____/ \___/ \__|___/ /_/   \_\_| |_|\__,_| |____/ \___/_/\_\___||___/                                                                                
#       
###########################
botName='UndeepBoxes'
botName='4386_20B_8550-defbot'


import random
import json

from collections import deque 

# These are the only additional libraries available to you. Uncomment them
# to use them in your solution.
#
import numpy    # Base N-dimensional array package
#import pandas   # Data structures & analysis

# Constant corresponding to differents players
__PLAYER_ID__ = 0
__ENEMY_ID__  = 1
__EMPTY_ID__  = -1 


# Constants concerning the game board
__NB_CELLS__        = 16
__NB_CELLS_TO_WIN__ = 8
__NB_LINES__        = 0


# Alpha Beta Related Constants
__DEPTH__ = 1
__ALPHA__ = -float('Inf')
__BETA__  =  float('Inf')


# Game stage compared to the number of empty lines
__RANDOM_PART__     = 30
__EARLY_GAME__      = 24
__EARLY_MID_GAME__  = 18
__MID_GAME_01__     = 14
__MID_GAME_02__     = 10
__MID_GAME_END__    = 8
__END_GAME__        = 3

# Heuristics To Use
__HEURISTIC_NUMBER_BOXES__  = True
__HEURISTIC_ENDGAME__       = True
__HEURISTIC_DYNAMIC_COUNT__ = False



#######################
#                     #
#                     #
#    PROVIDED FUNC    #
#                     #
#                     #
#######################
# =============================================================================
# This calculate_move() function is where you need to write your code. When it
# is first loaded, it will play a complete game for you using the Helper
# function that is defined below.

# calculate_move() gets as input a JSON object "gamestate" which contains all the information from the current game.
# It needs to return a move for the player to make,
# which consists of two coordinates (a,b) and (c,d)
# written in the form "[[a,b],[c,d]]"
def calculate_move(gamestate):
    m = gamestate["Dimensions"][0]; n = gamestate["Dimensions"][1]
    
    # Update the number of cells contained on the board
    __NB_CELLS__ = ( (m - 1) * (n - 1) )
    __NB_CELLS_TO_WIN__ = __NB_CELLS__ / 2
    
    # Update Alpha Value for Alpha Beta to the number of boxes / 2 +1 
    __ALPHA__ = - (__NB_CELLS_TO_WIN__ + 1) 
    
    return StrategySelector(gamestate)
    
    
    
    

# This function is given a list of the lines on the board, where each line
# is written in the form [[a,b],[c,d],x]
# where (a, b) and (c,d) are the coordinates
#   and x is -1 if neither player has made that line
#       and otherwise is the index of the player (0 or 1) who has made the line
# (You are player 0)
# The function returns all legal moves, where a move
#   consists of two coordinates representing adjacent dots
def find_legal_moves(grid):
    legal_moves = []
    for x in grid:
        if x[2] == -1: # then neither player has made this move
            legal_moves.append([x[0], x[1]])
    return legal_moves


# Unused helper function
# which may be useful in checking if you can complete a square
# Its input is the line that a player wants to draw as their move
#   (which must be a legal move)
# and a list of squares on the board, where each square is
# written as [[l0, l1, l2, l3], x]
#   where l0,...,l3 are the four lines that make up the square
#       written in the form [[a,b],[c,d],b] where (a,b), (c,d) are the coordinates
#       and b is a Boolean to indicate if the line has been played yet
#   and x is -1 if this square has not been completed
#       and otherwise is the index of the player who completed it
def does_complete_square(move, squares):
    for square in squares:
        for line in square[0]: # square[0] contains the four lines
            if [line[0], line[1]] == move:
                # find the lines l in the square which are already complete
                # (they are complete if the Boolean l[2] is True)
                lines_already_complete = list(filter(lambda l: l[2], square[0]))
                num_lines_complete = len(lines_already_complete)
                if num_lines_complete == 3:
                    # then the line 'move' is the fourth line in the square
                    return True
    # if there are no squares containing the line with three completed lines already
    return False




#######################
#                     #
#        MOVES        #
#     CALCULATION     #
#                     #
#######################
def StrategyAteFirst(gamestate, depth_offset):
    alphaBetaMover = AlphaBeta(gamestate)
    (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=__DEPTH__ + depth_offset, killer_moves_enabled=True)
    return ret
 

def StrategyLongTermPlaying(gamestate, depth_offset):
    alphaBetaMover = AlphaBeta(gamestate)
    (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=__DEPTH__ + depth_offset, killer_moves_enabled=False)
    return ret
 

def StrategySelector(gamestate):
    (_, _, empty_lines) = nb_lines_placed(gamestate["Grid"]) 

    res = None
    if empty_lines < __END_GAME__:
        res = StrategyAteFirst(gamestate, __END_GAME__)            # Default: 5    # Max: 10
    elif(empty_lines < __MID_GAME_END__):
        res = StrategyLongTermPlaying(gamestate, 9)     # Default: 6    # Max: 8
    elif(empty_lines < __MID_GAME_02__):
        res = StrategyLongTermPlaying(gamestate, 8)     # Default: 4    # Max: 8
    elif(empty_lines < __MID_GAME_01__):
        res = StrategyLongTermPlaying(gamestate, 2)     # Default: 2    # Max: 3
    elif(empty_lines < __EARLY_MID_GAME__):
        res = StrategyLongTermPlaying(gamestate, 1)     # Default: 2    # Max: 2
    elif(empty_lines < __EARLY_GAME__):
        res = StrategyAteFirst(gamestate, 1)            # Default: 1    # Max: 1
    elif(empty_lines > __RANDOM_PART__):
        res = EarlyGameMoveCalculation(gamestate)
    else:
        res = StrategyAteFirst(gamestate, 1)            # Default: 1    # Max: 1

    return res
"""
    Local Tournament with 100 games vs housebot-competition:
        * Depth [3, 4, 3, 1, 0, 0]
            * Won = 54,  Drawn = 22, Lost = 24  |   0.54
        * Depth [3, 3, 2, 1, 0, 0]
            * Won = 50,  Drawn = 18, Lost = 32  |   0.5
        * Depth [5, 6, 4, 2, 2, 0]
            * Won = 63,  Drawn = 23, Lost = 26  |   0.5625
        * Depth [5, 6, 4, 2, 1, 1]
            * Won = 68,  Drawn = 15, Lost = 18  |   0.6733
            * Won = 58,  Drawn = 16, Lost = 26  |   0.58
        * Depth [8, 9, 3, 2, 1, 1]
            * Won = 112, Drawn = 41, Lost = 75  |   0.4912
        * Depth [EG,9, 8, 5, 1, 1, 1]  
            * Won = 51, Drawn = 27, Lost = 22   |   0.51

"""

    
    

'''
Return True if the move in parameter 
completes any boxes of the game.

Deprecated. 

Use StrategySelector(gamestate: Gamestate) function instead.

Parameters: 
    gamestate (gamestate): Board Gamestate

Returns: 
    int: Best Move Available using differents algorithms
'''
def calculateNextMove_wrapper(gamestate):
    alphaBetaMover = AlphaBeta(gamestate)
    (player_lines, enemy_lines,empty_lines) = nb_lines_placed(gamestate["Grid"]) 
    
    ret = None
    # Run AlphaBeta algorithm with differents parameters depending of the game advancement
    if(empty_lines < __END_GAME__):
        (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=__DEPTH__ + 3, killer_moves_enabled=True)
    elif(empty_lines < __MID_GAME_END__):
        (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=__DEPTH__ + 3, killer_moves_enabled=False)
    elif(empty_lines < __MID_GAME__):
        (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=__DEPTH__ + 2, killer_moves_enabled=False)
    elif(empty_lines < __EARLY_MID_GAME__):
        (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=__DEPTH__ + 1, killer_moves_enabled=False)
    elif(empty_lines < __EARLY_GAME__):
        (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=__DEPTH__ + 0, killer_moves_enabled=True)
    else:
        (_,ret) = alphaBetaMover.alpha_beta_main_wrapper(depth=0, killer_moves_enabled=True)
        #return EarlyGameMoveCalculation(gamestate) #Deprecated
    return ret
    
    
 

    
#####################
#                   #
#     UTILITIES     #
#                   #
#####################


'''
Simple Function claiming any boxes available, if possible.
Otherwise, plays a random move
Kind of Deprecated

Parameters: 
    gamestate (gamestate): Board Gamestate

Returns: 
    int: Best Move Available (First which completes a boxes, or random)
'''
def EarlyGameMoveCalculation(gamestate):
    legal_moves = find_legal_moves(gamestate["Grid"])
    x = legal_moves[random.randint(0, len(legal_moves)-1)]
    
    # If it can complete a box, return it
    for move in legal_moves:
        if does_complete_square(move, gamestate["Squares"]):
            return move
            
    # Else, if it do not create any completable box, return it
    for move in legal_moves:
        if not does_create_completable_boxe(move, gamestate["Squares"]):
            return move
            
    return x




'''
Return the number of boxes with either three, two or one lines

Parameters: 
    squares (list): squares list coming from the gamestate

Returns: 
    int: Number of C-Box (three lines)
    int: Number of boxes composed of two lines
    int: Number of boxes with only one line
'''
def numberCapturableBoxes(squares):
    triple_line_box = 0
    double_line_box = 0
    single_line_box = 0
    for square in squares:
        for line in square[0]: # square[0] contains the four lines
            # find the lines l in the square which are already complete
            # (they are complete if the Boolean l[2] is True)
            lines_already_complete = list(filter(lambda l: l[2], square[0]))
            num_lines_complete = len(lines_already_complete)
            if num_lines_complete == 3:
                #print("Box with 3 lines will be claimable")
                triple_line_box += 1
            if num_lines_complete == 2:
                #print("Box with 2 lines will be claimable")
                double_line_box += 1
            if num_lines_complete == 1:
                #print("Box with 1 lines will be claimable")
                single_line_box += 1
    return (triple_line_box, double_line_box, single_line_box)
    
    
'''
return the number of lines placed by each players
and the number of empty lines.
Mostly used to determine the progression of the
game.

Parameters: 
    grid (int[]): list coming from the gamestate

Returns: 
    int: Number of lines placed by the player
    int: Number of lines placed by the opponent
    int: Number of empty lines
'''
def nb_lines_placed(grid):
    occupied_enemy = 0 
    occupied_player = 0 
    empty_cell = 0
    
    for line in grid:
        (x, y, val) = line
        if val is __PLAYER_ID__:
            occupied_player += 1
        elif val is __ENEMY_ID__:
            occupied_player += 1
        else:
            empty_cell +=1
    return (occupied_player, occupied_enemy, empty_cell)
    

'''
Return True if the move in parameter 
completes any boxes of the game.

Parameters: 
    move ([int,int,int]): The move to test
    squares (list): squares list coming from the gamestate

Returns: 
    Boolean: Return true if its complete a box. False otherwise.
'''
def does_create_completable_boxe(move, squares):
    for square in squares:
        for line in square[0]: # square[0] contains the four lines
            if [line[0], line[1]] == move:
                # find the lines l in the square which are already complete
                # (they are complete if the Boolean l[2] is True)
                lines_already_complete = list(filter(lambda l: l[2], square[0]))
                num_lines_complete = len(lines_already_complete)
                if num_lines_complete == 2:
                    # then the line 'move' is the fourth line in the square
                    return True
    # if there are no squares containing the line with three completed lines already
    return False
    
#####################
#                   #
#    HEURISTICS     #
#                   #
#####################

'''
Return the number of C-box

Parameters: 
    gamestate (gamestate): Board Gamestate

Returns: 
    int: return the number of boxes that can be claim in a row (C-box)
'''
def heuristic_can_claim_boxes(gamestate):
    result = 0
    for square in gamestate["Squares"]:
        for line in square[0]: # square[0] contains the four lines
            # find the lines l in the square which are already complete
            # (they are complete if the Boolean l[2] is True)
            lines_already_complete = list(filter(lambda l: l[2], square[0]))
            num_lines_complete = len(lines_already_complete)
            if num_lines_complete == 3:
                # then the line 'move' is the fourth line in the square
                result = result + 1
    return result
    
    
'''
Heuristic calculation in an attempt for Chain Boxes detection and evaluation
Deprecated and not really working. Need more works.

Parameters: 
    gamestate (gamestate): Board Gamestate

Returns: 
    int: Weighted Heuristic Value
'''
def heuristic_chain_boxes(gamestate):
    (three_lines, two_line, one_line) = numberCapturableBoxes(gamestate["Squares"])
    
    if (three_lines == 1) and two_line > 2:
        three_lines = -2 - three_lines
    return 75*three_lines - 25*two_line + 1*one_line


    
'''
Simple Heuristic calculation for score
Return the difference between the number
of boxes claimed by the player and its opponent

Parameters: 
    gamestate (gamestate): Board Gamestate

Returns: 
    int: Weighted Heuristic Value
'''
def heuristic_number_boxes_claimed(gamestate):
    enemy = gamestate["OppScore"]
    myPlayer = gamestate["MyScore"]
    score = myPlayer - enemy
    #print(score)
    return score

   
'''
Heuristic Calculation to test Extreme cases.
Mostly if the player or its opponent has more 
than half of the available boxes.

Parameters: 
    gamestate (gamestate): Board Gamestate

Returns: 
    int: Return Beta if Player will win, 
            Alpha if the opponent will. 
            Otherwise, return 0 and will be ignored
'''
def heuristic_end_game_killer_move(gamestate):
    enemy = gamestate["OppScore"]
    myPlayer = gamestate["MyScore"]
    if(enemy > __NB_CELLS_TO_WIN__):
        return __ALPHA__
    if(myPlayer > __NB_CELLS_TO_WIN__):
        return __BETA__
    return 0
    

'''
Main heuristic function which is making the sum of each sub-heuristics

Parameters: 
    gamestate (gamestate): Board Gamestate
    nextPlayer(int): next player id (currently deprecated)

Returns: 
    int: Board evaluation value
'''  
def heuristic(gamestate, nextPlayer):
    score = 0
    if __HEURISTIC_NUMBER_BOXES__:  # DEFAULT: True
        score += heuristic_number_boxes_claimed(gamestate)
    
    if __HEURISTIC_DYNAMIC_COUNT__: # DEFAULT: False
        score += heuristic_chain_boxes(gamestate) #Too much time consuming
        
    if __HEURISTIC_ENDGAME__:       # DEFAULT: True
        score += heuristic_end_game_killer_move(gamestate)
    
    return score
    
    
    
    
##################
#                #
#   ALPHA-BETA   #
#                #
##################
class AlphaBeta:
    def __init__(self, game_input):
        self.gamestate = game_input.copy()
        self.move_played = deque()
        
    

    '''
    Simulate a move pushing and store it in a LIFO queue
    
    Finally, its update the whole board to refresh the number of boxes claimed 
    by each players
    
    Parameters: 
        move (int): the move to simulate
        player_id (int): the player id
    '''
    def __SimulatePushMove(self, move, player_id):
        #indice = 0
        i = 0
        for cell in self.gamestate["Grid"]:
            (l,r,_) = cell
            if(l == move[0] and r == move[1]):
                self.gamestate["Grid"][i] = (l,r,player_id)
                break
            i = i + 1
        self.__UpdateBoxes(player_id, [l,r])
        self.move_played.append(i)
    
    


    '''
    Simulate a move poping and store it in a LIFO queue
    
    Its simply pop the last elem from the queue that has been pushed (containing the indice of the grid cell)
    get the left and right dot with l and r variable and update it has empty.
    
    Finally, its update the whole board to refresh the number of boxes claimed 
    by each players
    '''
    def __SimulatePopMove(self):
        d = self.move_played.pop()
        (l,r,_) = (self.gamestate["Grid"][d])
        self.gamestate["Grid"][d] = (l,r, __EMPTY_ID__)
        self.__UpdateBoxes(__EMPTY_ID__, [l,r])
        
        

    '''
    Local private function to update the whole board 
    (including score) after a player pushing/poping move.
    
    
    Parameters: 
        player_id (int): player making the move
        move (int[]): move coordinates
    '''
    def __UpdateBoxes(self, player_id, move):
        i = 0
        squares = self.gamestate["Squares"]
        
        for square in squares:
            res = []
            updateSquare = False
            for line in square[0]: # square[0] contains the four lines
                if [line[0], line[1]] == move:
                    #iToUpdate.append(i)
                    if player_id is __EMPTY_ID__:
                        res.append([line[0], line[1], False])
                    else:
                        res.append([line[0], line[1], True])
                    updateSquare = True
                        
                else:
                    res.append(line)
                    
                        
            if updateSquare:
                lines_already_complete = list(filter(lambda l: l[2], res))
                num_lines_complete = len(lines_already_complete)
                if num_lines_complete == 4:
                    self.gamestate["Squares"][i][1] = player_id
                    
                    if player_id is __ENEMY_ID__:
                        self.gamestate["OppScore"] += 1
                    elif player_id is __PLAYER_ID__:
                        self.gamestate["MyScore"] += 1
                    else:
                        pass
                else:
                    cp = self.gamestate["Squares"][i][1]
                    self.gamestate["Squares"][i][1] = __EMPTY_ID__
                    if cp is __ENEMY_ID__:
                        self.gamestate["OppScore"] -= 1
                    elif cp is __PLAYER_ID__:
                        self.gamestate["MyScore"] -= 1
                    else:
                        pass
                    
            self.gamestate["Squares"][i][0] = res
            
            i = i + 1
                
    

    '''
    Sort the current legal moves to optimize it.
    
    First, we are saving those which complete at least one box.
    Then, we put those which will NOT create a completable box for the enemy.
    Finally, wwe concatenate this list with the others move.
    
    Parameters: 
        gamestate (gamestate): Board Gamestate
      
    Returns: 
        int: Description of return value 
    '''
    def GetSortedLegalMoves(self, gamestate):
        moves = find_legal_moves(self.gamestate["Grid"])
        box_claiming_array  = []
        box_claimable_array = []
        
        # Add the move that will close a box
        for move in moves:
            if does_complete_square(move, self.gamestate["Squares"]):
                box_claiming_array.append(move)
                moves.remove(move)
        
        
        # Add the moves that will create a C-box for the opponent 
        for move in moves:
            if not does_create_completable_boxe(move, self.gamestate["Squares"]):
                box_claimable_array.append(move)
                moves.remove(move)
        
        return box_claiming_array + box_claimable_array + moves
        
    


    '''
    Return the initial alpha value.
    Used a method to prevent __ALPHA__ value modification
      
    Returns: 
        int: __ALPHA__
    '''
    def __alpha__(self):
        return __ALPHA__
    

    '''
    Return the initial beta value.
    Used a method to prevent __BETA__ value modification
      
    Returns: 
        int: __BETA__
    '''
    def __beta__(self):
        return __BETA__

    

    '''
    A wrapper for the Alpha-Beta pruning Algorithm. This function manages
    the result returned by each path analysis from the currently
    available moves.
    
    Parameters: 
        depth (int): The Maximum Default Depth of the tree
        killer_moves_enabled (Boolean): Activation or not of killer moves
    
    Returns: 
        int: Corresponding score of the selected move. For debugging purpose.
        int[]: Best move decided by the algorithm
    '''
    def alpha_beta_main_wrapper(self,
        depth = 2,
        killer_moves_enabled=False
    ):
        
        moves =  self.GetSortedLegalMoves(self.gamestate)
        
        # Pick the first Move of the list to prevent none return
        return_move = moves[0]
            
        bestscore = self.__alpha__()
        
        for move in moves:
            nextPlayer = __ENEMY_ID__
            
            if does_complete_square(move, self.gamestate["Squares"]):
                if killer_moves_enabled:
                    nextPlayer = __PLAYER_ID__
                    return(self.__beta__(), move)
            
            
            self.__SimulatePushMove(move, __PLAYER_ID__)
            if nextPlayer is __ENEMY_ID__:
                (score, _)  = self.__min_score_alpha_beta(depth, bestscore, self.__beta__(), killer_moves_enabled, __ENEMY_ID__)
            else:
                (score, _)  = self.__max_score_alpha_beta(depth, bestscore, self.__beta__(), killer_moves_enabled, __PLAYER_ID__)
            self.__SimulatePopMove()
            
            if score > bestscore:
                bestscore = score
                return_move = move
        
                
        return (bestscore, return_move)


    

    '''
    Return True if the result of the game has been decided
    Actually, the game is over since any of the player have
    more than the number of boxes / 2 or the sums of both
    player and opponent are greater (for safety) or equals
    the numbers of boxes.
    
    Returns: 
        Boolean: Game is Over or not 
    '''
    def __is_game_over(self):
        score_me = self.gamestate['MyScore']
        score_en = self.gamestate['OppScore']
        if score_me > __NB_CELLS_TO_WIN__:
            return True
        if score_en > __NB_CELLS_TO_WIN__:
            return True
        
        
        score = score_en + score_me
        if score >= __NB_CELLS__:
            return True
        return False
        
        
        

    '''
    Max layer of the A-B tree. Return the heuristic value if
    the game is over or the depth has reached 0.
    
    If the game is over, we also return the depth that still need to be checked
    since a game can be over when any player have more than half available
    boxes.
    
    
    While simulating the moves, it is important to note that a player can plays
    multiple times in a row. That is why we are doing the separation between
    the __PLAYER_ID__ and the __ENEMY_ID__.
    
    Finally, we are updating beta value, pruning if required and returning the best value.
    completes any boxes of the game.
    
    Parameters: 
        depth (int): "default" depth of the A-B tree 
        alpha (int): current alpha value 
        beta (int): current beta value 
        killer_moves_enabled (bool): Boolean to enable/disable killer moves 
        nextPlayer (int): Integer corresponding to the current player ID 
  
    Returns: 
        int: score
        int: remaining depth - 1 OR 0 
    '''
    def __max_score_alpha_beta(self, depth, alpha, beta, killer_moves_enabled=False, nextPlayer=__PLAYER_ID__):
        if depth == 0 or self.__is_game_over():  # leaves of alpha-beta pruning    
            d_offset = depth - 1
            if depth is 0:
                d_offset = 0
            return (heuristic(self.gamestate, __PLAYER_ID__), d_offset)
    
        moves =  self.GetSortedLegalMoves(self.gamestate)
        maxVal = alpha
        d_offset = 0
        for move in moves: 
            d_tmp = 0
            nextPlayer = __ENEMY_ID__
            
            if does_complete_square(move, self.gamestate["Squares"]):
                nextPlayer = __PLAYER_ID__
            
            self.__SimulatePushMove(move, __PLAYER_ID__)
            if nextPlayer is __PLAYER_ID__:
                (score, d_tmp) = self.__max_score_alpha_beta(depth-1, alpha, beta, killer_moves_enabled, __PLAYER_ID__)
            else:
                (score, d_tmp) = self.__min_score_alpha_beta(depth-1, alpha, beta, killer_moves_enabled, __ENEMY_ID__)
                if depth is 1:
                    score = score - 1
            depth = depth + d_tmp
            d_offset += d_tmp
            self.__SimulatePopMove()
            
            if score > maxVal:
                maxVal = score
            if maxVal >= beta:
                return (maxVal, d_offset + depth - 1)
                # return (maxVal, depth-1) # d_offset + depth - 1)
            if maxVal > alpha:
                alpha = maxVal
            
        #return (maxVal, d_offset)
        return (maxVal, 0)
    
    
    
        

    '''
    Min layer of the A-B tree. Return the heuristic value if
    the game is over or the depth has reached 0.
    
    If the game is over, we also return the depth that still need to be checked
    since a game can be over when any player have more than half available
    boxes.
    
    
    While simulating the moves, it is important to note that a player can plays
    multiple times in a row. That is why we are doing the separation between
    the __PLAYER_ID__ and the __ENEMY_ID__.
    
    Finally, we are updating alpha value, pruning if required and returning the minimal value.
    completes any boxes of the game.
    
    Parameters: 
        depth (int): "default" depth of the A-B tree 
        alpha (int): current alpha value 
        beta (int): current beta value 
        killer_moves_enabled (bool): Boolean to enable/disable killer moves 
        nextPlayer (int): Integer corresponding to the current player ID 
  
    Returns: 
        int: score
        int: remaining depth - 1 OR 0 
    '''
    def __min_score_alpha_beta(self, depth, alpha, beta, killer_moves_enabled=False, nextPlayer=__ENEMY_ID__):
        if depth == 0 or self.__is_game_over():
            d_offset = depth - 1
            if depth is 0:
                d_offset = 0
            return (heuristic(self.gamestate, __ENEMY_ID__), d_offset)
        
        moves =  self.GetSortedLegalMoves(self.gamestate)
        minVal = beta
        d_offset = 0
        for move in moves:
            nextPlayer = __PLAYER_ID__
            d_tmp = 0
            
            if does_complete_square(move, self.gamestate["Squares"]):
                nextPlayer = __ENEMY_ID__
                if killer_moves_enabled:
                    return (alpha, depth - 1)
                    
                
            self.__SimulatePushMove(move, __ENEMY_ID__)
            if nextPlayer is __PLAYER_ID__:
                (score, d_tmp) = self.__max_score_alpha_beta(depth-1, alpha, beta, killer_moves_enabled, __PLAYER_ID__)
            else:
                (score, d_tmp) = self.__min_score_alpha_beta(depth-1, alpha, beta, killer_moves_enabled, __ENEMY_ID__)
            depth = depth + d_tmp
            d_offset += d_tmp
            self.__SimulatePopMove()
            
            
            if score < minVal:
                minVal = score
            if minVal <= alpha:
                return (minVal, d_offset + depth - 1)
            if minVal > beta:
                beta = minVal
            
        return (minVal, 0)
      
