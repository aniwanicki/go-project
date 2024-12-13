"""
Fake implementations of GoBase.

We provide a GoStub implementation, and you must
implement a GoFake implementation.
"""
from copy import deepcopy

from base import GoBase, BoardGridType, ListMovesType
#### define Queue class 


class GoStub(GoBase):
    """
    Stub implementation of GoBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.

    - The board is always initialized with four pieces in the four
      corners of the board. Player 1 has pieces in the northeast and
      southwest corners of the board, and Player 2 has pieces in the
      southeast and northwest corners of the board.
    - Players are allowed to place pieces in any position of the board
      they want, even if there is already a piece in that position
      (placing a piece in such a position replaces the previous piece
      with the new one). The ko and superko rule do not apply.
    - The game ends after four moves. Whatever player has a piece in
      position (0,1) wins. If there is no piece in that position,
      the game ends in a tie.
    - The scores are always reported as 100 for Player 1 and 200 for
      Player 2. Note how the scores do not play a role in determining
      the outcome of the game.
    - It does not validate board positions. If a method is called with
      a position outside the board, the method will likely cause an exception.
    - It does not implement the load_game or simulate_moves method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, superko: bool = False):
        """
        See GoBase.__init__
        """
        if players != 2:
            raise ValueError(
                "The stub implementation " "only supports two players"
            )

        super().__init__(side, players, superko)

        self._grid = [[None] * side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        """
        See GoBase.grid
        """
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        See GoBase.turn
        """
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        """
        See GoBase.available_moves
        """
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        """
        See GoBase.done
        """
        return self._num_moves == 4

    @property
    def outcome(self) -> list[int]:
        """
        See GoBase.outcome
        """
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [1, 2]
        else:
            return [self._grid[0][1]]

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        """
        See GoBase.piece_at
        """
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        See GoBase.legal_move
        """
        return True

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        See GoBase.apply_move
        """
        r, c = pos
        self._grid[r][c] = self._turn
        self.pass_turn()

    def pass_turn(self) -> None:
        """
        See GoBase.pass_turn
        """
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def scores(self) -> dict[int, int]:
        """
        See GoBase.scores
        """
        return {1: 100, 2: 200}

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        See GoBase.load_game
        """
        raise NotImplementedError

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        """
        See GoBase.simulate_move
        """
        raise NotImplementedError

################################################ define queue class
class Queue:
    lst: list[tuple[int, int, int]]

    def __init__(self):
        self.lst = []

    def __str__(self) -> str:
        return str(self.lst)
    def enqueue(self, value: tuple[int,int,int]) -> None:
        self.lst.insert(0, value)

    def dequeue(self) -> tuple[int,int,int]:
        return self.lst.pop()
    
    def queue_length(queue):
        return len(queue)
    
    @property
    def frozen_value(self) -> tuple[int, int, int]:
        return tuple(self.lst)

class Stack:
    lst: list[tuple[int,int,int]]

    def __init__(self):
        self.lst = []

    def push(self, value):
        self.lst.append(value)

    def pop(self):
        return self.lst.pop()

    def stack_top(self):
        return self.lst[-1]

    def stack_is_empty(self):
        return len(self.lst) == 0
    
################################################## class GoFake
class GoFake(GoBase):

    _grid: list[list[int | None]]
    _turn: int
    _num_moves: int
    _game_over: bool
    _done: bool
    _winners: list[int]
    qeues_encountered: set
    _current_move: list[int]
    _is_legal: bool
    _all_moves: str
    _av_moves: list[tuple]
    _score_dict: dict[int:int]
    _move_list: list[list[int,int,int]]

    def __init__(self, side: int, players: int, superko: bool = False):
        if side <= 4:
            raise ValueError("board is smaller than allowed 4x4")
        self._side = side
        if players != 2:
            raise ValueError("GoFake only supports two players")
        self._players = players
        self._superko = superko

        self._grid = [[None] * side for _ in range(side)]
        #for _ in range(side):
        #    self._grid.append([None]*side)
        self._num_moves = 0
        self._turn = 1
        self._game_over = False
        self._done = False
        self._winners = []
        self._score_dict = {}
        self._is_legal = True
        self._queue = Queue()
        self._current_move = [0,0, self._turn]
        self._moves_encountered = set()
        self._all_moves = "" #m = makes move, p = pass
        self._move_tuple = tuple
        self._captured = Stack()
        self._move_list = [[]]
        self._av_moves = []

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players
    @property    
    def grid(self) -> BoardGridType:
        
        return deepcopy(self._grid)
    @property
    def size(self) -> int:
        return self._side
    @property
    def turn(self) -> int:
        return self._turn
    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        total = []
        for r in range(self.size):
            for c in range(self.size):
                total.append((r,c))
                if self._grid[r][c] == None:
                    moves.append((r, c))

        return moves
    
    @property
    def done(self) -> bool:
        consec_passes = "p" * self.num_players
        if self._grid[0][0] != None:
            self._done == True
        elif consec_passes in self._all_moves:
            self._done == True
        else:
            self._done == False
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
            for player in score_dict:
                if score_dict[player] == high:
                    winner_list.append(player)

        return winner_list
    
    def piece_at(self, pos: tuple[int, int]) -> int | None:
        xcoord = pos[0]
        ycoord = pos[1]

        return self._grid[xcoord][ycoord]
        
    def legal_move(self, pos: tuple[int, int]) -> bool:
        if pos == None:
            self._is_legal = True
        else:
            self._is_legal = True
            xcoord = pos[0]
            ycoord = pos[1]
            if xcoord< 0 or xcoord > (self.size -1):
                raise ValueError("Out of Bounds")
            elif ycoord< 0 or ycoord > (self.size -1):
                raise ValueError("Out of Bounds")
            elif type(self._grid[xcoord][ycoord]) == int:
                self._is_legal = False
            elif not self._captured.stack_is_empty():
                lastx = self._current_move[0]
                lasty = self._current_move[1]
                last_captured = self._captured.stack_top()
                x = pos[0]
                y = pos[1]
                attempt = tuple([x,y,self._turn])
                #check for ko
                if (x == (lastx + 1) or x == (lastx - 1)) and y == lasty:
                    if (last_captured[0] == attempt[0]) & (last_captured[1] == attempt[1]) & (last_captured[2] != attempt[2]):
                        self._is_legal = False
                if (y == (lasty + 1) or y == (lasty - 1)) and x == lastx:
                    if (last_captured[0] == attempt[0]) & (last_captured[1] == attempt[1]) & (last_captured[2] != attempt[2]):
                        self._is_legal = False   
                #check for superko
                if self._superko:
                    attempt = [x,y,self._turn]
                    if attempt in self._move_list:
                        self._is_legal = False

        return self._is_legal
            

    def apply_move(self, pos: tuple[int, int]) -> None: #this is janky coding. using both
        if pos == (0,0):                                #lists, tuples, queues, and sets. must 
            self._done = True                           #be a way to simplify
            self._grid[0][0] = self._turn
            for i in self.available_moves:
                x = i[0]
                y = i[1]
                self._grid[x][y] = self._turn
        if pos in self.available_moves and pos != (None or (0,0)):
            input = pos
            xcoord = input[0]
        
            ycoord = input[1]
        
            adjx_list = [xcoord - 1, xcoord + 1]
            adjy_list = [ycoord - 1, ycoord + 1]
        
            for x in adjx_list:
                if x==self.size or x<0:
                    adjx_list.remove(x)
                
            for y in adjy_list:    
                if y==self.size or y<0:
                    adjy_list.remove(y)

            for x in adjx_list:
                if self._grid[x][ycoord] != None and self._grid[x][ycoord] != self._turn:
                
                    self._grid[x][ycoord] = None
                    self._captured.push((x,ycoord, self._turn))
            for y in adjy_list:
                if self._grid[xcoord][y] != None and self._grid[xcoord][y] != self._turn:
                
                    self._grid[xcoord][y] = None
                    self._captured.push((xcoord,y, self._turn))
        
            self._grid[xcoord][ycoord] = self._turn
            self._current_move = [xcoord, ycoord, self._turn]
            self._move_tuple = (xcoord, ycoord, self._turn)
            self._move_list.append([xcoord, ycoord, self._turn])

            self._queue.enqueue(self._move_tuple)
        
            self._moves_encountered.add(self._queue.frozen_value)
            self._all_moves = self._all_moves + "b"
            if self._turn == self.num_players:
                self._turn = 1
            else:
                self._turn += 1
            
            #print(self._all_moves)
            
        
        elif pos == None:
            self.pass_turn()
             

    def pass_turn(self) -> None:
        self._all_moves = self._all_moves + "p"
        consec_passes = "p" * self.num_players
        if consec_passes in self._all_moves:
            self._done = True
        if self._turn == self.num_players:
            self._turn = 1
        else:
            self._turn += 1
        
        
    def scores(self) -> dict[int, int]:
        score = {}
        for i in range(self.num_players):
            score[i+1] = 0
        
        for j in range(self.size):
            for k in range(self.size):
                if self._grid[j][k] != None:
                    piece = self._grid[j][k]
                    score[piece] = score[piece]+ 1
                    
        return score
        

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError 
    
    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        new = GoFake(self._side, self._players, self._superko)
        new._grid = self.grid #from grid method/property CHANGED
        new._turn = self._turn
        new._current_move = self._current_move
        new._players = self.num_players
        new._side = self.size
        new._captured = self._captured
        new._move_tuple = self._move_tuple
        new._queue = self._queue
        new._moves_encountered = self._moves_encountered
        new._all_moves = self._all_moves
        new.apply_move(pos)

        return new


