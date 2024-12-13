import pytest
from abc import ABC
from base import GoBase
from go import Go

#test for constructing Go game; vary sizes but only 2 players
def test_inheritance() -> None: #test 1
    """Test that Go inherits from GoBase"""
    assert issubclass(Go, GoBase), "GoFake should inherit from GoBase"

def test_construction_1() -> None: #test 2
    """Test that a Go object is constructed correctly"""
    test_go = Go(19, 2, False)
    grid = test_go.grid

    assert len(grid) == 19
    assert not test_go.done


def test_construnction_2() -> None: #test 3
    """Test that a Go object is constructed correctly"""
    test_go = Go(7, 2, False)
    grid = test_go.grid

    assert len(grid) == 7
    assert not test_go.done


#test for 19x19 Go game. test size, num_players, turn, 
#piece_at, legal_move, and available_moves

def test_size_1() -> None: #test 4
    """Test that a 19x19 Go game size property is accurate"""
    go = Go(19,2)
    assert go.size == 19

def test_num_players_1() -> None: #test 5
    """Test that a 19x19 Go game players property is accurate"""
    go = Go(19,2)
    assert go.num_players == 2

def test_turn_1() -> None: #test 6
    """Test that a 19x19 Go game turn property is accurate. No play has been
    made, so should just be 1"""
    go = Go(19,2)
    assert go.turn == 1

def test_piece_at_1() -> None: #test 7
    """Test that a 19x19 Go game has no pieces on board at start"""
    go = Go(19,2)
    for i in range(19):
        for j in range(19):
            pos = (i,j)
            assert go.piece_at(pos) == None


def test_legal_move_1() -> None: #test 8
    """Test that a 19x19 Go game starts with all legal moves on board"""
    go = Go(19,2)
    for i in range(19):
        for j in range(19):
            pos = (i,j)
            assert go.legal_move(pos) == True

def test_available_move_1() -> None: #test 9
    """Test that a 19x19 Go game has all available moves on start"""
    go = Go(19,2)
    
    moves = go.available_moves
    assert len(moves) == 19 * 19
    for row in range(go.size):
        for col in range(go.size):
            assert (row, col) in moves

#test for 19x19 Go games. test apply_move on legal pos, and make sure 
#turn and piece_at return correct values. verify done and outcome remain
#consistent as the game is still live
def test_apply_move_1() -> None: #test 10
    """Test that a 19x19 Go can place a legal piece identified by player"""
    go = Go(19,2)
    pos = (15,15)
    assert go.turn == 1
    assert go.legal_move(pos)
    go.apply_move(pos)
    assert go.turn == 2
    assert go.piece_at(pos) == 1
    assert go.done == False
    assert go.outcome == []

#test for 19x19 Go game. test apply_move on intersection that won't cause
#any captures. Make both players pass, and confirm grid has expected pieces 
#and outcome and done return accurately
def test_apply_move_2() -> None: #test 11
    """Test that multiple pieces can be placed. Once game is over, pieces
    should be in same location to calculate score."""
    go = Go(19,2)
    assert go.done == False
    pos = (2,3)
    assert go.legal_move(pos)
    go.apply_move(pos)
    pos = (11,15)
    assert go.legal_move(pos)
    go.apply_move(pos)
    pos = (5,6)
    assert go.legal_move(pos)
    go.apply_move(pos)
    
    go.pass_turn()
    go.pass_turn()

    assert go.done == True
    assert go.piece_at((2,3)) == 1
    assert go.piece_at((11,15)) == 2
    assert go.piece_at((5,6)) == 1
    
    assert go.outcome == [1]

def test_apply_move_3() -> None: #test 12
    """Test that making moves with no captures, then both players passing, returns
    a grid with correct pieces, outcome returns the winner (tie), and game is done"""
    go = Go(19,2)
    assert go.done == False
    pos = (1,1)
    assert go.legal_move(pos)
    go.apply_move(pos)
    pos = (11,15)
    assert go.legal_move(pos)
    go.apply_move(pos)
    pos = (5,6)
    assert go.legal_move(pos)
    go.apply_move(pos)
    pos = (9,3)
    assert go.legal_move(pos)
    go.apply_move(pos)
    
    go.pass_turn()
    go.pass_turn()
    assert go.done == True
    assert go.piece_at((1,1)) == 1
    assert go.piece_at((11,15)) == 2
    assert go.piece_at((5,6)) == 1
    assert go.piece_at((9,3)) == 2
    
    assert go.outcome == [1,2]
#########################################################################
# MILESTONE 2 TESTS
#########################################################################

def test_init_9x9_size_1() -> None: #test 13
    go = Go(9,2)
    assert go.size == 9

def test_init_9x9_players_1() -> None: #test 14
    go = Go(9,2)
    assert go.num_players == 2

def test_init_9x9_turn_1() -> None: #test 15
    go = Go(9,2)
    assert go.turn == 1

def test_init_9x9_piece_at_1() -> None: #test 16
    go = Go(9,2)
    for i in range(go.size):
        for j in range(go.size):
            pos = (i,j)
            assert go.piece_at(pos) == None

def test_init_9x9_legal_move_1() -> None: #test 17
    go = Go(9,2)
    for i in range(go.size):
        for j in range(go.size):
            pos = (i,j)
            assert go.legal_move(pos)

def test_init_9x9_available_moves_1() -> None: #test 18
    go = Go(9,2)
    moves = go.available_moves
    assert len(moves) == go.size * go.size
    for i in range(go.size):
        for j in range(go.size):
            assert (i,j) in moves

def test_init_13x13_size_1() -> None: #test 19
    go = Go(13,2)
    assert go.size == 13

def test_init_13x13_players_1() -> None: #test 20
    go = Go(13,2)
    assert go.num_players == 2

def test_init_13x13_turn_1() -> None: #test 21
    go = Go(13,2)
    assert go.turn == 1

def test_init_13x13_piece_at_1() -> None: #test 22
    go = Go(13,2)
    for i in range(go.size):
        for j in range(go.size):
            pos = (i,j)
            assert go.piece_at(pos) == None

def test_init_13x13_legal_move_1() -> None: #test 23
    go = Go(13,2)
    for i in range(go.size):
        for j in range(go.size):
            pos = (i,j)
            assert go.legal_move(pos)

def test_init_13x13_available_moves_1() -> None: #test 24
    go = Go(13,2)
    moves = go.available_moves
    assert len(moves) == go.size * go.size
    for i in range(go.size):
        for j in range(go.size):
            assert (i,j) in moves

def test_init_19x19_legal_move_1() -> None: #test 25
    go = Go(19,2)
    for i in range(go.size):
        for j in range(go.size):
            pos = (i,j)
            assert go.legal_move(pos)

def test_init_19x19_available_moves_1() -> None: #test 26
    go = Go(19,2)
    moves = go.available_moves
    assert len(moves) == go.size * go.size
    for i in range(go.size):
        for j in range(go.size):
            assert (i,j) in moves

def test_19x19_make_2_moves_1() -> None: #test 27
    go = Go(19,2)
    moves = [(8,4), #1
             (3,13), #2
             ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)

    assert go.piece_at((8,4)) == 1
    assert go.piece_at((3,13)) == 2
    assert go.turn == 1

def test_19x19_move_is_illegal_1() -> None: #test 28
    go = Go(19,2)
    assert go.legal_move((8,4))
    moves = [(8,4), #1
             ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    assert go.piece_at((8,4)) == 1
    assert not go.legal_move((8,4))


def test_19x19_pass_turn_1() -> None: #test 29
    go = Go(19,2)
    moves = [(12,16), #1
             ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.pass_turn()
    assert go.turn == 1

def test_19x19_both_pass_done_1() -> None: #test 30
    go = Go(19,2)
    moves = [(3,0), #1
             ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1

    go.load_game(turn, grid)
    go.pass_turn()
    go.pass_turn()
    assert go.done

def test_apply_move_with_adj_1() -> None: #additional, for troubleshooting
    # test that surrounding one piece removes that piece
    #     b           b
    #   b w b #->   b   b
    #     b           b
    go = Go(6,2)
    moves = [(2,4), #1
             (2,3), #2
             (1,3), #1
    ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    assert go.piece_at((2,3)) == 2
    go.pass_turn()
    go.apply_move((2,2))
    go.pass_turn()
    go.apply_move((3,3))

    assert go.piece_at((2,4)) == 1
    assert go.piece_at((1,3)) == 1
    assert go.piece_at((2,2)) == 1
    assert go.piece_at((3,3)) == 1
    assert go.piece_at((2,3)) == None

    
def test_apply_move_with_adj_2() -> None: #additional, for troubleshooting
    #test that surrounding a piece on the edge removes that piece
    go = Go(6,2)
    moves = [(0,0), #1
             (1,0), #2
             (4,2), #1 #just to not use apply_move or add extra lines for turn
    ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.apply_move((0,1))

    assert go.piece_at((0,1)) == 2
    assert go.piece_at((1,0)) == 2
    assert go.piece_at((4,2)) == 1
    assert go.piece_at((0,0)) == None

def test_apply_move_with_adj_3() -> None: #additional, for troubleshooting
    #test that surrounding two connect pieces removes both
    #    b    #->    b    
    #  b w b  #->  b   b  
    #  b w b  #->  b   b  
    #    b    #->    b    
    go = Go(6,2)
    moves = [(1,3), #1
             (2,3), #2
             (2,2), #1 
             (3,3), #2 
             (3,2), #1
             None,
             (4,3), #1
             None,
             (3,4), #1
             None
    ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        if move != None:
            x = move[0]
            y = move[1]
            grid[x][y] = turn
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
        else:
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
    go.load_game(turn, grid)
    go.apply_move((2,4))

    assert go.piece_at((1,3)) == 1
    assert go.piece_at((2,2)) == 1
    assert go.piece_at((3,2)) == 1
    assert go.piece_at((4,3)) == 1
    assert go.piece_at((3,4)) == 1
    assert go.piece_at((2,4)) == 1
    assert go.piece_at((2,3)) == None
    assert go.piece_at((3,3)) == None


def test_single_captured_piece_1() -> None:
    #Verify that one piece is removed when captured in 19x19 game
    #   o
    #  oxo
    #   o
    go = Go(19,2)
    moves = [(5,5), #1
             (4,5), #2
             (0,1), #1 
             (6,5), #2 
             (3,2), #1
             (5,4), #2
             (12,14), #1
    ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
            x = move[0]
            y = move[1]
            grid[x][y] = turn
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1

    go.load_game(turn, grid)
    go.apply_move((5,6))

    assert go.piece_at((5,5)) == None
    assert go.piece_at((4,5)) == 2
    assert go.piece_at((0,1)) == 1
    assert go.piece_at((6,5)) == 2
    assert go.piece_at((3,2)) == 1
    assert go.piece_at((5,4)) == 2
    assert go.piece_at((12,14)) == 1

def test_multiple_captured_pieces_1() -> None:
    #   b b b b
    # b w w w w b
    # b w b b w b
    #   b     b 
    go = Go(19,2)
    moves = [(7,5), #1
             (8,5), #2
             (7,6), #1 
             (9,5), #2 
             (7,7), #1
             (8,6), #2
             (7,8), #1
             (8,7), #2
             (8,4), #1
             (8,8), #2
             (9,4), #1
             (9,8), #2
             (10,5), #1
             (1,5), #2
             (9,6), #1
             (3,15), #2
             (9,7), #1
             (3, 13), #2
             (10,8), #1
             (16,16), #2
             (9,9), #1
             (15,2), #2
    ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
            x = move[0]
            y = move[1]
            grid[x][y] = turn
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1

    go.load_game(turn, grid)
    assert go.piece_at((8,5)) == 2
    assert go.piece_at((9,5)) == 2
    assert go.piece_at((8,6)) == 2
    assert go.piece_at((8,7)) == 2
    assert go.piece_at((8,8)) == 2
    assert go.piece_at((9,8)) == 2
    assert go.piece_at((1,5)) == 2
    assert go.piece_at((3,15)) == 2
    assert go.piece_at((3,13)) == 2
    assert go.piece_at((16,16)) == 2
    assert go.piece_at((15,2)) == 2

    go.apply_move((8,9))
    
    assert go.piece_at((8,5)) == None
    assert go.piece_at((9,5)) == None
    assert go.piece_at((8,6)) == None
    assert go.piece_at((8,7)) == None
    assert go.piece_at((8,8)) == None
    assert go.piece_at((9,8)) == None
    assert go.piece_at((1,5)) == 2
    assert go.piece_at((3,15)) == 2
    assert go.piece_at((3,13)) == 2
    assert go.piece_at((16,16)) == 2
    assert go.piece_at((15,2)) == 2

def test_simple_ko_19x19() -> None:
    go = Go(19,2)
    moves = [(6,4), #1
             (6,5), #2
             (5,5), #1 
             (5,6), #2 
             (7,5), #1
             (7,6), #2
             (3,2), #1
             (6,5), #2
    ]
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
            x = move[0]
            y = move[1]
            grid[x][y] = turn
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
    go.load_game(turn, grid)
    go.apply_move((6,6))
    assert go.piece_at((6,6)) == 1
    assert go.piece_at((6,5)) == None
    assert not go.legal_move((6,5))
##superko
def test_simpleko_19x19_2() -> None:
    #Test for simpleko- This is what will be used to test superko, but under 
    #simple moves the X location should be a valid move. 
    #
    #     b w              #->     b w              #->     b w              
    #   b w   w            #->   b   b w            #->   b w   w            
    #     b w       w b    #->     b w       w b    #->     b w       w b    
    #             w b   b  #->             w   w b  #->             w X w b  
    #               w b    #->               w b    #->               w b    
    moves = [
        (2,3), #1
        (2,4), #2
        (1,4), #1
        (1,5), #2
        (3,4), #1
        (3,5), #2
        (4,9), #1
        (2,6), #2
        (3,10), #1
        (4,8), #2
        (4,11), #1
        (3,9), #2
        (5,10), #1
        (5,9), #2
    ]
    go = Go(19,2, False)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
            x = move[0]
            y = move[1]
            grid[x][y] = turn
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
    go.load_game(turn, grid)
    go.apply_move((2,5))
    assert not go.legal_move((2,4))
    go.apply_move((4,10))
    assert not go.legal_move((4,9))
    go.pass_turn()
    assert go.legal_move((2,4))
    go.apply_move((2,4))
    assert go.legal_move((4,9))

def test_superko_19x19_1() -> None:
    #Test for superko- the position where the X is should be an invalid move.
    #
    #     b w              #->     b w              #->     b w              
    #   b w   w            #->   b   b w            #->   b w   w            
    #     b w       w b    #->     b w       w b    #->     b w       w b    
    #             w b   b  #->             w   w b  #->             w X w b  
    #               w b    #->               w b    #->               w b   
    #cannot use load game as it removes memory needed from apply_move 
    moves = [
        (2,3), #1
        (2,4), #2
        (1,4), #1
        (1,5), #2
        (3,4), #1
        (3,5), #2
        (4,9), #1
        (2,6), #2
        (3,10), #1
        (4,8), #2
        (4,11), #1
        (3,9), #2
        (5,10), #1
        (5,9), #2
    ]
    go = Go(19,2,True)
    for move in moves:
        go.apply_move(move)
    go.apply_move((2,5))
    assert not go.legal_move((2,4))
    go.apply_move((4,10))
    assert not go.legal_move((4,9))
    go.pass_turn()
    assert go.legal_move((2,4))
    go.apply_move((2,4))
    assert not go.legal_move((4,9)) #superko 

def test_19x19_no_territories_score_1():
    moves = [
        (1, 3), #1
        (6, 18), #2
        (15, 9), #1
        (12, 10), #2
        (4, 5), #1
        (5, 1), #2
        (7, 14), #1
        (9, 10), #2
        (1, 17), #1
        (18, 2), #2
        (16, 6) #1
    ]

    go = Go(19, 2)

    for move in moves:
        go.apply_move(move)
    scores = go.scores()
    assert scores[1] == 6
    assert scores[2] == 5
def test_19x19_no_territories_score_load_game_1():
    #This makes the same moves as the previous tests but uses the load game method
    #rather than apply move
    moves = [
        (1, 3), #1
        (6, 18), #2
        (15, 9), #1
        (12, 10), #2
        (4, 5), #1
        (5, 1), #2
        (7, 14), #1
        (9, 10), #2
        (1, 17), #1
        (18, 2), #2
        (16, 6) #1
    ]

    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)

    scores = go.scores()
    assert scores[1] == 6
    assert scores[2] == 5

def test_19x19_no_territories_score_2():
    moves = [
        (1, 3), #1
        (6, 18), #2
        None, #1
        (12, 10), #2
        (4, 5), #1
        (5, 1), #2
        None, #1
        (9, 10), #2
        None, #1
        (18, 2), #2
        (16, 6) #1
    ]

    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    
    for move in moves:
        if move != None:
            x = move[0]
            y = move[1]
            grid[x][y] = turn
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
        else:
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
    go.load_game(turn, grid)

    scores = go.scores()
    assert scores[1] == 3
    assert scores[2] == 5

def test_19x19_with_territories_score_1():
    #creates territory from captured pieces
    #       w
    #     b b b
    #   b w w w b
    #     b b w b
    #   w     b
    # This creates a capture of 4 white pieces, giving black a territory of 4.
    #White also has 2 pieces in the adjacent area to confirm they aren't included.
    moves = [     
        (2, 2), #1
        (2, 3), #2
        (1,3), #1
        (2,4), #2
        (1, 4), #1
        (2, 5), #2
        (1,5), #1
        (3, 5), #2
        (3,3), #1
        (0,4), #2
        (3, 4), #1
        (4,2), #2
        (4,5), #1
        (15,15), #2
        (3,6), #1
        (13,3), #2
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.apply_move((2,6))
    scores = go.scores()
    assert scores[1] == 13
    assert scores[2] == 4

def test_19x19_with_territories_score_2():
    #creates territory from surrounding empty pieces, not captures.
    # this test also tests for capturing territories against the borders
    #   w
    # w     w
    #     b b b        w w
    #   b       b    w     w
    #     b b   b    w     w w
    #         b      w         w
    #     b            w w w w 
    #   b   b
    #   b   b
    #     b
    moves = [     
        (8, 1), #1
        (0, 1), #2
        (9, 1), #1
        (4,12), #2
        (8, 3), #1
        (1, 3), #2 #2's solo piece; no territory
        (9, 3), #1
        (17,0), #2
        (7, 2), #1
        (2, 10), #2
        (12,0), #1
        (2,11), #2
        (2, 2), #1
        (3,9), #2
        (2, 3), #1
        (4,9), #2
        (2, 4), #1
        (5,9), #2
        (3, 1), #1
        (6,10), #2
        (4, 2), #1
        (6,11), #2
        (4, 3), #1
        (6,12), #2
        (5, 4), #1
        (6,13), #2
        (4, 5), #1
        (5,14), #2
        (10,12), #1
        (4,13) #2
        ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    print(go._territory_list, "territories before creation")
    go.apply_move((3,5))
    go.apply_move((1,0))
    go.apply_move((10,2))
    go.apply_move((3,12))
    print(go._territory_list, "territories")

    scores = go.scores()
    assert scores[1] == 23
    assert scores[2] == 26

def test_19x19_with_territories_score_3():
    #creates territory from surrounding empty pieces and captures.
    # this test also tests for capturing territories against the borders
    #     w b b              ##->      w b b
    # w w b w w b       b     ##-> w w b     b       b
    #   w w b b       b   b   ##->   w w b b       b   b    + random pieces elsewhere
    #       w           b                w           b
    # w w w   b                    w w w   b
    moves = [     
        (0, 3), #1
        (1, 3), #2
        (0, 4), #1
        (1,4), #2 
        (6,5), #1
        (0, 2), #2 
        (15,14), #1 
        (1,0), #2
        (2,3), #1
        (9,8), #2 
        (2,4), #1 
        (2,1), #2
        (2, 8), #1
        (4,2), #2
        (2, 10), #1
        (3,3), #2
        (9, 2), #1
        (4,0), #2
        (3, 9), #1
        (4,1), #2
        (4,4), #1  
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.pass_turn()
    go.apply_move((1,5))
    go.apply_move((1,1))
    go.apply_move((1,9))
    go.pass_turn()
    go.apply_move((1,2)) #1

    scores = go.scores()
    assert scores[1] == 17
    assert scores[2] == 11

def test_19x19_no_territories_outcome_1():
    #places pieces that do NOT make territories, 
    #passes and confirms outcome is a tie

    moves = [     
        (0, 3), #1
        (0, 8), #2
        (5, 7), #1
        (6,3), #2  
        (7, 16), #1
        (8, 18), #2 
        (10,0), #1 #solo piece
        (12,4), #2
        (1,14), #1 #captures white piece, cannot take back by ko
        (16, 15), #2

        ]
     
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.pass_turn()
    go.pass_turn()

    scores = go.scores()
    assert scores[1] == 5
    assert scores[2] == 5
    winner = go.outcome
    assert len(winner) == 2
    assert winner[0] == 1
    assert winner[1] == 2

def test_19x19_no_territories_outcome_2():
    #places pieces that do NOT make territories, 
    #passes and confirms player 1 is winner

    moves = [     
        (0, 3), #1
        (0, 8), #2
        (5, 7), #1
        (6,3), #2  
        (7, 16), #1
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.pass_turn()
    go.apply_move((10,0))
    go.pass_turn()
    go.apply_move((1,14))
    go.pass_turn()
    go.pass_turn()

    scores = go.scores()
    assert scores[1] == 5
    assert scores[2] == 2
    winner = go.outcome
    assert len(winner) == 1
    assert winner[0] == 1

def test_19x19_with_territories_outcome_1():
    #creates territory from surrounding empty pieces and captures.
    # this test also tests for capturing territories against the borders
    #   b w b b       w w    ##->  b   b b       w w   
    #   b w w w b   w     w  ##->  b       b   w     w  
    #     b b w w b   w w    ##->    b b     b   w w    
    #         b w b b b b    ##->        b   b b b b        
    #         b w w w w w b  ##->        b           b       
    #           b b b b b    ##->          b b b b b    
    moves = [     
        (0, 1), #1
        (0, 2), #2
        (0, 3), #1
        (1,2), #2  
        (0, 4), #1
        (1, 3), #2 
        (1,1), #1
        (1,4), #2
        (1,5), #1
        (2,4), #2  
        (2,3), #1 
        (2,5), #2
        (2,2), #1
        (3,5), #2
        (2,6), #1
        (4,5), #2
        (16,17),#1
        (4,6), #2
        (3,4), #1 
        (4,7), #2
        (4,4), #1
        (4,8), #2
        (5,5), #1
        (4,9), #2
        (5,6), #1
        (0,9), #2
        (5,7), #1
        (0,8), #2
        (5,8), #1 
        (1,7), #2
        (5,9), #1
        (1,10), #2
        (4,10), #1
        (2,9), #2
        (3,9), #1
        (2,14), #2
        (3,8), #1
        (12,0),#2
        (3,7), #1
        (13,5), #2
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.apply_move((3,6))
    go.apply_move((2,8))
    go.pass_turn()
    go.pass_turn()
    scores = go.scores()
    assert scores[1] == 33
    assert scores[2] == 11
    winner = go.outcome
    assert len(winner) == 1
    assert winner[0] == 1

def test_19x19_with_territories_outcome_2():
    #creates territory from surrounding empty pieces and captures.
    # this test also makes sure empty spaces that are not surrounded by one player
    # are not territories
    #       b w    ##->    w   b w   ##->    w   b w   
    #b    b w   w  ##->  b   b   b w ##->  b   b w   w 
    #       b w    ##->    b   b w   ##->    b   b w   
    #
    # 
    moves = [     
        (0, 3), #1
        (0, 4), #2
        (1, 2), #1
        (1,3), #2  
        (2, 3), #1
        (1, 5), #2 
        (1,0), #1 #solo piece
        (15,15), #2  
        (10,10), #1 
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.apply_move((2,4))
    go.apply_move((1,4))
    go.apply_move((9,0))
    go.apply_move((7,12))
    go.apply_move((1,3))
    go.pass_turn()
    go.pass_turn()

    scores = go.scores()
    assert scores[1] == 6
    assert scores[2] == 7
    winner = go.outcome
    assert len(winner) == 1
    assert winner[0] == 2

#
def test_3player_19x916go_1():
    moves = [     
        (1, 3), #1
        (4, 4), #2
        (12, 16), #3
    ]
    go = Go(19, 3)
    for move in moves:
        go.apply_move(move)

    assert go.piece_at((1,3)) == 1
    assert go.piece_at((4,4)) == 2
    assert go.piece_at ((12,16)) == 3

def test_3player_19x916go_2():
    go = Go(19,3)
    pos = (5,3)
    go.apply_move(pos)
    go.pass_turn()
    go.pass_turn()
    go.pass_turn()

    assert go.piece_at((5,3)) == 1
    assert go.done == True



def test_simulate_move_1() -> None:
    """
    Test that simulating a move creates a new game
    """

    go = Go(19,2)

    new_go = go.simulate_move((15, 5))

    # Check that the original Go object has not been modified
    assert go.piece_at((15, 5)) is None
    assert go.turn == 1

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((15, 5)) == 1
    assert new_go.turn == 2


def test_simulate_move_2() -> None:
    """
    After making a few moves, check that simulating a move
    correctly creates a new game.
    """
    moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 0),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 0),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (13, 2),
    ]

    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)

    new_go = go.simulate_move((5, 5))

    # Check that the original GoFake object has not been modified
    assert go.piece_at((5, 5)) is None
    for move in moves:
        assert go.piece_at(move) is not None
    assert go.turn == 1

    # Check that the move was applied in the new GoFake object
    assert new_go.piece_at((5, 5)) == 1
    for move in moves:
        assert new_go.piece_at(move) is not None
    assert new_go.turn == 2


def test_simulate_move_3() -> None:
    """
    UPDATE DOCSTRING
    """
    moves = [
        (5, 6), #1
        (5, 5), #2
        (5, 4), #1
        (0, 3), #2
        (4, 5), #1
        (10, 15), #2
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    new_go = go.simulate_move((6, 5))


    # Check that the original Go object has not been modified
    assert go.piece_at((5, 6)) == 1
    assert go.piece_at((5, 5)) == 2
    assert go.piece_at((5, 4)) == 1
    assert go.piece_at((4,5)) == 1
    assert go.piece_at((0,3)) == 2
    assert go.piece_at((10,15)) == 2
    assert go.piece_at((6, 5)) is None
    assert go.turn == 1

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 5)) is None
    assert new_go.piece_at((6, 5)) == 1
    assert new_go.turn == 2


def test_simulate_move_4() -> None:
    """
    Check that simulating a pass works correctly.
    """
    go = Go(19, 2)

    new_go = go.simulate_move(None)

    # Check that the original Go object has not been modified
    assert go.turn == 1

    # Check that the pass was applied in the new Go object
    assert new_go.turn == 2


def test_simulate_move_5() -> None:
    """
    Check that simulating two consecutive passes works correctly.
    """
    go = Go(19, 2)

    new_go = go.simulate_move(None).simulate_move(None)

    # Check that the original Go object has not been modified
    assert go.turn == 1
    assert not go.done

    # Check that the passes were applied in the new Go object
    assert new_go.done

def test_grid_1() -> None:
    """Check that grid for an empty game is exported correctly"""

    go = Go(19, 2)

    grid = go.grid

    for row in range(go.size):
        for col in range(go.size):
            assert grid[row][col] is None


def test_grid_2() -> None:
    """
    Check that grid returns a deep copy of the board's grid,
    and that modifying grid's return value doesn't modify
    the game's board
    """

    go = Go(19, 2)

    grid = go.grid

    grid[5][5] = 1

    assert go.piece_at((5, 5)) is None, (
        "grid() returned a shallow copy of the game's board. "
        "Modifying the return value of grid() should not "
        "affect the game's board."
    )


def test_grid_3() -> None:
    """
    Check that grid returns a correct copy of the board after making
    a few moves (none of the moves will result in a capture)
    """

    moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 0),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 0),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (12, 2),
    ]

    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    grid = go.grid

    for row in range(go.size):
        for col in range(go.size):
            assert grid[row][col] == go.piece_at((row, col))

def test_10_more_capture_pieces():
    moves = [     
        (2,4), #1
        (3,4), #2
        (2,5), #1
        (3,5), #2  
        (3, 3), #1
        (4, 4), #2 
        (4,3), #1 
        (4,5), #2  
        (5,3), #1 
        (5,4), #2
        (6,4), #1
        (5,5), #2
        (3,6), #1
        (5,6), #2
        (4,6), #1
        (5,7), #2
        (4,7), #1
        (6,6), #2
        (6,5), #1
        (6,7), #2
        (5,8), #1
        (7,6), #2
        (7,5), #1
        (8,6), #2
        (8,5), #1
        (9,6), #2
        (9,5), #1
        (9,7), #2
        (6,8), #1
        (9,8), #2
        (10,6), #1
        (3,13), #2
        (10,7), #1
        (4,12), #2
        (7,7), #1
        (4,14), #2
        (8,7), #1
        (5,12), #2
        (8,8), #1
        (5,14), #2
        (10,8), #1
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.apply_move((6,13))
    scores = go.scores()
    assert scores[1] == 21
    go.apply_move((9,9))
    scores = go.scores()
    assert go.piece_at((6,6)) == None
    assert scores[1] == 37
    assert scores[2] == 8

def test_19x19_2player_territories_with_neutral():
    #This produces player one with a territory of 2 by capture and a territory 
    #of one by surrounding an empty square. Player 2 has a territory of 3 
    #by surrounding empty squares. Positions (14,3) and (14,4) are a neutral
    #territory. 
    moves = [     
        (11,4), #1
        (12,4), #2
        (11,3), #1
        (12,3), #2  
        (12,2), #1
        (15,3), #2 
        (13,3), #1 
        (15,4), #2  
        (13,4), #1 
        (14,5), #2
        (12,9), #1
        (16,6), #2
        (13,9), #1
        (17,6), #2
        (14,9), #1
        (18,6), #2
        (12,10), #1
        (16,8), #2
        (14,10), #1
        (17,8), #2
        (7,10), #1
        (18,8), #2
    ]
    go = Go(19, 2)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    go.load_game(turn, grid)
    go.apply_move((12,5))
    go.apply_move((14,2))
    go.apply_move((13,11))
    go.apply_move((15,7))
    scores = go.scores()

    assert scores[1] == 16
    assert scores[2] == 14

def test_19x19_3player_territories_with_neutral():
    #This produces player one with a territory of 2 by capture and a territory 
    #of one by surrounding an empty square. Player 2 has a territory of 3 
    #by surrounding empty squares. Positions (14,3) and (14,4) are a neutral
    #territory. 
    moves = [     
        (11,4), #1
        (12,4), #2
        (12,14), #3
        (11,3), #1
        (12,3), #2
        (12,15), #3  
        (12,2), #1
        (15,3), #2 
        (12,16), #3
        (13,3), #1 
        (15,4), #2
        (12,17), #3  
        (13,4), #1 
        (14,5), #2
        (12,18), #3
        (12,9), #1
        (16,6), #2
        (13,14), #3
        (13,9), #1
        (17,6), #2
        (14,14), #3
        (14,9), #1
        (18,6), #2
        (15,14), #3
        (12,10), #1
        (16,8), #2
        (16,14), #3
        (14,10), #1
        (17,8), #2
        (17,14), #3
        (7,10), #1
        (18,8), #2
    ]
    go = Go(19, 3)
    grid = []
    turn = 1
    for _ in range(go.size):
        grid.append([None]*go.size)
    for move in moves:
        x = move[0]
        y = move[1]
        grid[x][y] = turn
        if turn < go.num_players:
            turn = turn + 1
        elif turn == go.num_players:
            turn = 1
    go.load_game(turn, grid)
    go.apply_move((14,2))#3
    go.apply_move((12,5)) #1
    go.apply_move((15,7)) #2
    go.apply_move((18,14)) #3
    go.apply_move((13,11)) #1
    
    scores = go.scores()

    assert scores[1] == 16
    assert scores[2] == 13
    assert scores[3] == 36
    

