#go! in src
from abc import ABC, abstractmethod
from typing import Optional
from base import GoBase, BoardGridType, ListMovesType
from copy import deepcopy
import copy


class Board:

    _rows: int
    _cols: int
    #grid: list[list[Optional[int]]]
    _grid: BoardGridType

    def __init__(self, rows:int, cols:int):
        self._rows = rows
        self._cols = cols
        self._grid = []
        self.captured_list = []
        for _ in range(self._rows):
            self._grid.append([None]*self._cols)
        #print(self._grid, "grid")
        
    def set(self, row:int, col:int, value: Optional[int]) -> None:
        #could throw error for invalid move here
        row = row
        col = col
        self._grid[row][col] = value
        
    def get(self, row:int, col:int) -> Optional[int]:
        if row < 0 or row > (self._rows-1):
            #(row, "row")
            raise ValueError("Illegal Move")
        elif col < 0 or col > (self._cols-1):
            raise ValueError("Illegal Move")
        else: 
            return self._grid[row][col]
        
    def print_board(self) -> tuple[tuple[int]]:
        intermediate_list = []
        
        
        for i in range(len(self._grid)):
            switch_list = []
            for row in self._grid:
                switch_list.append(row[i])
            row_tuple = tuple(switch_list)
            intermediate_list.append(row_tuple)
        board_tuple = tuple(intermediate_list)
        return board_tuple




class Go(GoBase):

    _side: int
    _players: int
    _superko: bool
    _board: Board
    _done: bool
    _all_moves: set[tuple[int,int,int]]
    _connected: bool
    _connected_list: list[tuple[int,int]]
    _captured_list: list[tuple[int,int,int]]
    _surrounded_by: list[int]
    _empty_connected: list[tuple[int,int]]
    _connected_captured: list[tuple[int,int]]

    def __init__(self, side: int, players: int, superko: bool = False):
      
        super().__init__(side, players, superko)
        self._board = Board(side,side)
        self._game_string = ""
        self._done = False
        self._is_legal = True
        self._turn =1 
        self._all_moves = set() #set to compare if move has been made before, ko
        self._simple_moves = [] #treat like stack
        self._territory_list = []
        for _ in range(self._side):
            self._territory_list.append([None]*self._side)
        self._connected_captured = []
        self._group_dict = {}
        self.own_group = []
        self._surr_bool = False
        self._multiplayer_terr = []

    #
    # PROPERTIES
    #
    @property
    def size(self) -> int:
        return self._side

    @property
    def num_players(self) -> int:
        return self._players

    @property
    def grid(self) -> BoardGridType:
        return copy.deepcopy(self._board._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self._board.get(r,c) == None:
                    moves.append((r, c))
        return moves
        
    @property
    def done(self) -> bool: #done by filling the board, not by passing
        moves = self.available_moves
        if len(moves) == 0:
            self._done = True
        return self._done
       
    @property
    def outcome(self) -> list[int]:
        winner_list = []
        score_list = []
        score_dict = self.scores()
        if self.done:
            for player in score_dict:       
                score_list.append(score_dict[player])
            high = max(score_list)
            #print(score_dict, "score dict")
            for player in score_dict:
                if score_dict[player] == high:
                    winner_list.append(player)

        return winner_list
    
    #
    # METHODS
    #

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        x = pos[0]
        y = pos[1]
        return self._board.get(x,y)

    def legal_move(self, pos: tuple[int, int]) -> bool:
        self._is_legal = True
        if pos != None:
            piece = self.piece_at(pos)
            if piece != None:
                self._is_legal = False
            else:

                if len(self._simple_moves) > 0:
                    new_board = copy.deepcopy(self._board) #check privacy
                    new_board._grid = copy.deepcopy(self._board._grid)
                    new_board.set(pos[0], pos[1], self._turn)
                    ko_board = new_board.print_board()
                    last_ko = self._simple_moves.pop()
                    if ko_board == last_ko:
                        self._is_legal = False
                if self._superko == True:
                    if len(self._all_moves) > 0:
                        new = deepcopy(self)
                        new._board.set(pos[0], pos[1], new._turn)
                        captured = new.player_captured(pos[0], pos[1], new._turn)
                        new._multiplayer_terr = []
                        new._connected_list = []
                        new._surrounded_by = []
                        new._empty = 0
                        if not captured:
                            new.self_captured(pos[0], pos[1], new._turn)
                            new._connected_list = []
                            new._surrounded_by = []
                            new._empty = 0
                            new._multiplayer_terr = []
                        ko_board = new._board.print_board()
                        if ko_board in self._all_moves:
                            self._is_legal = False

        return self._is_legal

    def apply_move(self, pos: tuple[int, int]) -> None:
        if pos is not None:
            if pos in self.available_moves:
                legal = self.legal_move(pos)
                if legal:
                    self._board.set(pos[0], pos[1], self.turn)
                    self._game_string = self._game_string + "b"
                    ko_board_tuple = self._board.print_board()
                    self._all_moves.add(ko_board_tuple)
                    captured = self.player_captured(pos[0], pos[1], self.turn)

                    self._connected_captured = []
                    self._group_dict = {}
                    self._multiplayer_terr = []

                    if not captured:
                        self.self_captured(pos[0], pos[1], self.turn)
                        self._multiplayer_terr = []
                        
                        

                else:
                    return None
            #moves = self.available_moves
            #if len(moves) < (self.size * self.size):
            self.empty_surrounded(pos[0], pos[1], self._turn)
            self._multiplayer_terr = []
            self._connected_captured = []
            self._group_dict = {}
            if self._turn == self._players:
                self._turn = 1
            else:
                self._turn += 1
        elif pos == None:
            self.pass_turn()
        else:
            return None
    
    def player_captured(self, row, col, turn) -> bool:
        """
        This checks to see if the move the current player applied results
        in capturing pieces of the opponent player in a territory. If it does, 
        those connected pieces are set to None, and the pieces in the territory
        are added to the territory list to increase the players score in score().
        This then returns true.  
        
        If this move did not end in capturing opponent pieces, it returns False
        to the apply_move() method to then check if a self_capture occurred instead. 

        Args:
            row: x position of the chosen move
            col: y position of the chosen move
            turn: the current turn as returned by self.turn

        Returns: None
        """
        opponents = self.opponent_pieces(row, col, turn) 
        if len(opponents) > 0:
            for player in opponents:
                coordinates = opponents[player]
                surrounded = self.check_liberties(coordinates, player)
                if surrounded:
                    ko_board_tuple = self._board.print_board()   
                    self._simple_moves.append(ko_board_tuple)
                            
                    for position in self._connected_captured:  
                        self._board.set(position[0], position[1], None)
                        self._territory_list[position[0]][position[1]] = self._turn
                        self._territory_list[row][col] = None
                    
                    return True
                else:
                    return False

    def self_captured(self, row, col, turn) -> bool:
        """
        This checks to see if the move the current player applied results
        in a self capture. If it does, the chosen position is set to None. 
        If this move completed a territory for capture for the opponent, all
        pieces connected to this player in the territory are set to None.

        Args:
            row: x position of the chosen move
            col: y position of the chosen move
            turn: the current turn as returned by self.turn

        Returns: None
        """
        #Checks if the current player made a move that invoked self-capture. 
        opponents = self.opponent_pieces(row, col, turn) 
        positions = [(row,col)]
        if len(opponents) == 1:
            self.captured = self.check_liberties(positions, self.turn)
            if self.captured:
                self._board.set(row,col, None)
                if len(self._connected_captured) > 0 and len(self._game_string)>1:
                    for piece in self._connected_captured:
                        self._board.set(piece[0], piece[1], None)


    def adjacent_to(self, row,col, player:int):
        
        border_count = 0
        opponent_count = 0
        opponent_dict = {}
        move_list: list[tuple[int,int]]
        own_move_list: list[tuple[int,int]]
        own_move_list = []
        empty_list: list[tuple[int,int]]
        empty_list = []
        own_count = 0
        empty_count = 0
        if row - 1 >= 0:
            border_count += 1
            pos = (row-1, col)
            piece = self.piece_at(pos)
            if piece == player:
                own_count = own_count + 1
                own_move_list.append((row-1, col))
            elif piece != player and piece != None:
                opponent_count += 1
                if piece not in opponent_dict:
                    opponent_dict[piece] = []
                move_list = opponent_dict[piece]
                move_list.append((row-1, col))
            else:
                empty_count += 1
                empty_list.append((row-1,col))
        #if row + 1 < len(self.grid):
        if row + 1 < self.size:
            border_count += 1
            pos = (row+1,col)
            piece = self.piece_at(pos)
            if piece == player:
                own_count = own_count + 1
                own_move_list.append((row+1, col))
            elif piece != player and piece != None:
                opponent_count += 1
                if piece not in opponent_dict:
                    opponent_dict[piece] = []
                move_list = opponent_dict[piece]
                move_list.append((row+1, col))
            else:
                empty_count += 1
                empty_list.append((row+1,col))
        if col - 1 >= 0:
            border_count += 1
            pos = (row, col-1)
            piece = self.piece_at(pos)
            if piece == player:
                own_count = own_count + 1
                own_move_list.append((row, col-1))
            elif piece != player and piece != None:
                opponent_count += 1
                if piece not in opponent_dict:
                    opponent_dict[piece] = []
                move_list = opponent_dict[piece]
                move_list.append((row, col-1))
            else:
                empty_count += 1
                empty_list.append((row,col-1))
        #if col + 1 < len(self.grid):
        if col + 1 < self.size:
            border_count += 1
            pos = (row, col+1)
            piece = self.piece_at(pos)
            if piece == player:
                own_count = own_count + 1
                own_move_list.append((row, col+1))
            elif piece != player and piece != None:
                opponent_count += 1
                if piece not in opponent_dict:
                    opponent_dict[piece] = []
                move_list = opponent_dict[piece]
                move_list.append((row, col+1))
            else:
                empty_count += 1
                empty_list.append((row,col+1))
        return (border_count, opponent_count, own_count, empty_count, opponent_dict, own_move_list, empty_list)
    
    
    def opponent_pieces(self, row:int, col:int, player:int):
        player = self.turn
        adj_tuple = self.adjacent_to(row,col, player)
        opponents = adj_tuple[4]
        return opponents
    
    def empty_surrounded(self, row:int, col:int, player:int):
        """
        This function is called in self.apply_move after checking if either 
        a capture of the opponent pieces or a self capture occured. It finds
        the pieces directly adjacent to the applied move that are empty, then
        sends those pieces to helper functions to iteratively perform a 
        depth first search on each of those pieces to find if they are bounded
        by pieces of the current player's turn, creating a territory. It does
        not return anything, but it updates the self._territory_list, which is
        a list of lists representing the board, and the value at each position
        is the value of the player who controls the territory, if one, or None.

        Args:
            row: x position of the applied move
            col: y position of the applied move
            player: the player who placed the last piece, as given by self._turn

        Returns: None
        """
        empty = self.adjacent_to(row,col,player)
        empty_pieces = empty[6]
        empty_copy = empty_pieces[:]
        for empties in empty_copy:
            pot_surrounded = self.helper_empty_surrounded(empties[0], empties[1])
            if not pot_surrounded:
                empty_pieces.remove(empties)
            else:
                connected_list = pot_surrounded
                for piece in connected_list:
                    self._territory_list[piece[0]][piece[1]] = self._turn
            

    def helper_empty_surrounded(self, row:int, col:int) -> bool|list[tuple[int,int]]:
        """
        This is a helper function called in self.empty_surrounded. This uses a 
        DFS approach to finding if a group of empty pieces have been surrounded, 
        making a territory for a specific player. This is in the case that the 
        territory is created solely by placing pieces around already empty pieces,
        not by capturing opposing pieces and setting that position to None. 
        If the current applied move did not create a territory around empty pieces, 
        this function returns None. If it did, the function returns a list of 
        the corrdinates of the empty pieces to self.empty_surrounded. 

        Args:
            row: x position of the empty pieces adjacent to the applied move
            col: y position of the empty pieces adjacent to the applied move



        Returns: False, if an empty territory was not created.
                A list of tuple[int,int] denoting the positions of the empty
                pieces in the created territory. 
        """
        connected = []
        pieces = []
        checked = set()
        pieces.append((row,col))
        moves = self.available_moves
        if len(moves) == (self.size*self.size) or len(moves) == ((self.size*self.size)-1):
            return False
        while len(pieces) != 0:
            check = pieces.pop()
            if check not in checked:
                checked.add(check)
                connected.append(check)
                adj = self.adjacent_to(check[0],check[1],None)
                adj_empty = adj[5]
                adj_opp = adj[4]
                for next_empty in adj_empty:
                    pieces.append(next_empty)
                for key in adj_opp:
                    if key != self.turn:
                        return False
                    if key == self.turn:
                        borders = adj_opp[key]
                        for border in borders:
                            not_ins = self.helper_add_pieces(check, border)
                            for not_terr in not_ins:
                                checked.add(not_terr)
            if len(pieces) == 0:
                return connected
    
                
    def helper_add_pieces(self, check: tuple[int,int], bordered: tuple[int,int]) -> list[tuple[int,int]]:
        """
        This is a helper function called in self.helper_empty_surrounded. If an
        empty piece was found to be adjacent to a piece of the current player 
        who made the move, as returned by self._turn, this function adds the rest 
        of the pieces in the row or column past that piece into the "checked" set, 
        as they must not be part of the surrounded territory. 

        Args:
            check: tuple coordinate of the empty piece
            bordered: tuple coordinate of the found adjacent current player piece. 

        Returns: 
                not_in_list: a list[tuple[int,int]] denoting the coordinates of 
                the pieces that cannot be in the territory and would waste time
                iterating through. 
        """
        not_in_list = []
        if check[0] < bordered[0]:
            not_in = list[range(bordered[0]+1, self.size + 1)]
            for i in not_in:
                not_in_list.append((i,check[1]))
        if check[0] > bordered[0]:
            not_in = list[range(0, bordered[0])]
            for i in not_in:
                not_in_list.append((i,check[1]))
        if check[1] < bordered[1]:
            not_in = list[range(bordered[1]+1, self.size+1)]
            for i in not_in:
                not_in_list.append((check[0], i))
        if check[1] > bordered[1]:
            not_in = list[range(0, check[1])]
            for i in not_in:
                not_in_list.append((check[0], i))
        return not_in_list

    def liberties(self, row:int, col:int, player:int):
        """
        This is a helper function for self.check_liberties(). It records the
        value of all the opposing players in adjacent areas, and adds a move 
        to a list of pieces if it is directly connected. This list is then accessed
        in apply_move to set all the pieces in the captured territory to None. 

        Args:
            move_list: list of the positions, as tuples of (int,int) of the opposing
                        pieces in the grid positions directly adjacent to the chosen piece. 
            player: the value of the opposing player in the adjacent positions, 
                    as returned by self.adjacent_to()


        Returns: bool
        """
        adj_positions = self.adjacent_to(row,col, player)
        if player not in self._multiplayer_terr:
            self._multiplayer_terr.append(player)
        position = (row,col)
        empty_adj_positions = adj_positions[6]
        if len(empty_adj_positions) == 0:
            self.own_group = adj_positions[5]
            if position not in self._connected_captured:
                self._connected_captured.append((row,col))
            self._group_dict[position] = True
            return False
        else:
            if len(empty_adj_positions) > 0:
                if position not in self._group_dict:
                    self._group_dict[position] = False
                return True
            
    def check_liberties(self, move_list: list[tuple[int,int]], player:int) -> bool:
        """
        This checks to see if the move the current player applied results
        in surrounding a group of opponent pieces. If all the opponent pieces in 
        that group have no liberties and are bounded, this method returns True. 
        If all the adjacent opponent pieces to the applied move, and those adjacent
        to those (etc), still have liberties, this move did not surround them 
        and the method returns False. 

        Args:
            move_list: list of the positions, as tuples of (int,int) of the opposing
                        pieces in the grid positions directly adjacent to the chosen piece. 
            player: the value of the opposing player in the adjacent positions, 
                    as returned by self.adjacent_to()


        Returns: bool
        """
        count = 0
        for move in move_list:
            if_liberties = self.liberties(move[0], move[1], player)
            if not if_liberties:
                adj = self.adjacent_to(move[0], move[1], player)
                total = adj[0]
                opponent = adj[1]
                own = adj[2]
                own_list = adj[5]
                if total == opponent:
                    self.surr_bool = True
                    return self.surr_bool
                elif total == opponent + own:
                    self.surr_bool = True
                    for own_piece in own_list:
                        count = 0
                        if own_piece not in self._connected_captured:
                            own_piece = [own_piece]
                            return self.check_liberties(own_piece, player)
                    for pieces in self._connected_captured:
                        adj2 = self.adjacent_to(pieces[0], pieces[1], player)
                        own_list = adj2[5]
                        if len(own_list) > 0:
                            for piece in own_list:
                                if piece not in self._connected_captured:
                                    piece = [piece]
                                    return self.check_liberties(piece, player)
                    for piece in self._group_dict:
                        if self._group_dict[piece] == True:
                            count = count + 1
                    if count == len(self._connected_captured):
                        return True                      
                else:
                    self._surr_bool = False
                    return self._surr_bool

        return self._surr_bool


   
    def pass_turn(self) -> None:
        self._game_string = self._game_string + "p"
        consec_passes = "p" * self._players
        if consec_passes in self._game_string:
            self._done = True
        if self._turn == self._players:
            self._turn = 1
        else:
            self._turn += 1
        

    
    def scores(self) -> dict[int, int]:
        score = {}
        for i in range(self.num_players):
            score[i+1] = 0 #sets all players to 0 at beginning

        for j in range(self.size):
            for k in range(self.size):
                move = (j,k)
                player = self.piece_at(move)
                if player != None:
                    score[player] = score[player] + 1
                    #print(j,k,"player", player, "score for placed piece")
                capt_terr = self._territory_list[j][k]
                if capt_terr != None:
                    score[capt_terr] = score[capt_terr] + 1

        return score
    
    def load_game(self, turn: int, grid: BoardGridType) -> None:

        if turn > self.num_players:
            raise ValueError
        else:
            self._turn = turn
        if len(grid) != self.size:
            raise ValueError
        else:
            assert len(grid) == self.size
        for i in range(self.size):
            for j in range(self.size):
                value = grid[i][j]
                if value != None and (value < 1 or value > self.num_players):
                    raise ValueError
                else:
                    self._board.set(i,j,value) 


    
    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        #new = Go(self._side, self._players, self._superko)
        #new._board = copy.deepcopy(self._board) #check privacy
        #new._board._grid = copy.deepcopy(self.grid)
        #new._turn = copy.deepcopy(self._turn)
        #new.available_moves = self.available_moves
        #new._players = self.num_players
        #new._side = self.size
        #new._all_moves = copy.deepcopy(self._all_moves)
        #new.apply_move(pos)
        new = deepcopy(self)
        new.apply_move(pos)
        return new
        


