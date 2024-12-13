from typing import Optional 
#interface should not be game specific
#tests in test_board.py
#need rows, cols, integer player number
class Board:

    _rows: int
    _cols: int
    _grid: list[list[Optional[int]]]

    def __init__(self, rows:int, cols:int):
        self._rows = rows
        self._cols = cols
        self._grid = []
        for _ in range(rows):
            self._grid.append([None]*cols)
        
    def set(self, row:int, col:int, value: Optional[int]) -> None:
        #could throw error for invalid move here
        row = row
        col = col
        self._grid[row-1][col-1] = value
        
    def get(self, row:int, col:int) -> Optional[int]:
        if row < 0 or row > (self._rows - 1):
            raise ValueError("Illegal Move")
        elif col < 0 or col > (self._cols - 1):
            raise ValueError("Illegal Move")
        else: 
            return self._grid[row-1][col-1]
    
    
