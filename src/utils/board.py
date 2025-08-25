from utils.enums.board_marker import BoardMarker


class Board:
  def __init__(self, size: int):
    self.board = [[(0, BoardMarker.EMPTY) for _ in range(size)] for _ in range(size)]

  def place_queen(self, row: int, col: int):
    self.board[row][col] = (self.board[row][col][0], BoardMarker.QUEEN)

  def remove_queen(self, row: int, col: int):
    self.board[row][col] = (self.board[row][col][0], BoardMarker.EMPTY)

  def place_blocker(self, row: int, col: int):
    self.board[row][col] = (self.board[row][col][0], BoardMarker.BLOCKED)

  def remove_blocker(self, row: int, col: int):
    self.board[row][col] = (self.board[row][col][0], BoardMarker.EMPTY)
  
  def is_empty(self, row: int, col: int) -> bool:
    return self.board[row][col][1] == BoardMarker.EMPTY

  def set_colour(self, row: int, col: int, colour: int):
    self.board[row][col] = (colour, self.board[row][col][1])