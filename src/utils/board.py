from utils.enums.board_event import BoardEvent
from utils.enums.board_marker import BoardMarker


class Board:
  def __init__(self, size: int):
    self.board = [[(0, BoardMarker.EMPTY) for _ in range(size)] for _ in range(size)]
    self.callbacks = {}

  def trigger_callback(self, event_type: BoardEvent, *args):
    if event_type in self.callbacks:
      self.callbacks[event_type](*args)

  def set_callback(self, event_type: BoardEvent, callback):
    self.callbacks[event_type] = callback

  def unset_callback(self, event_type: BoardEvent):
    if event_type in self.callbacks:
      del self.callbacks[event_type]

  def update_cell_colour(self, row: int, col: int, colour: int):
    self.board[row][col] = (colour, self.board[row][col][1])
    self.trigger_callback(BoardEvent.COLOUR_UPDATED, row, col, colour)

  def update_cell_marker(self, row: int, col: int, marker: BoardMarker):
    self.board[row][col] = (self.board[row][col][0], marker)
    if marker == BoardMarker.QUEEN:
      self.trigger_callback(BoardEvent.QUEEN_PLACED, row, col, marker)
    elif marker == BoardMarker.BLOCKED:
      self.trigger_callback(BoardEvent.BLOCKER_PLACED, row, col, marker)
    elif marker == BoardMarker.EMPTY:
      self.trigger_callback(BoardEvent.MARKER_REMOVED, row, col, marker)

  def place_queen(self, row: int, col: int):
    self.update_cell_marker(row, col, BoardMarker.QUEEN)

  def remove_marker(self, row: int, col: int):
    self.update_cell_marker(row, col, BoardMarker.EMPTY)

  def place_blocker(self, row: int, col: int):
    self.update_cell_marker(row, col, BoardMarker.BLOCKED)

  def is_empty(self, row: int, col: int) -> bool:
    return self.board[row][col][1] == BoardMarker.EMPTY

  def set_colour(self, row: int, col: int, colour: int):
    self.update_cell_colour(row, col, colour)