from collections import defaultdict
from utils.board import Board

def queens_solver(board: Board) -> Board:
  filtered_compartments = _filter_compartments(board)
  sorted_compartments = _sort_compartments(filtered_compartments)

  filled_colours = set()
  placed_queens = set()
  blocked_rows = [False] * len(board.board)
  blocked_cols = [False] * len(board.board)
  result = _place_queens(board, sorted_compartments, filled_colours, 
                         placed_queens, blocked_rows, blocked_cols)
  return result

def _filter_compartments(board: Board) -> Board:
  compartments = defaultdict(list)
  for row in range(len(board.board)):
    for col in range(len(board.board[row])):
      colour, _ = board.board[row][col]
      compartments[colour].append((row, col))
  return compartments

def _sort_compartments(compartments: dict[list]) -> dict:
  # Sort the compartments by their keys (e.g., 'queens', 'blocked')
  return dict(sorted(compartments.items(), key=lambda item: len(item[1])))

def _place_queens(board: Board, sorted_compartments: dict[int, list[tuple[int, int]]], 
                  filled_colours: set[int], placed_queens: set[tuple[int, int]], 
                  blocked_rows: list[bool], blocked_cols: list[bool]) -> Board:
  # Implement your backtracking algorithm here
  if len(filled_colours) == len(sorted_compartments):
    return board  # All compartments filled successfully

  for colour, positions in sorted_compartments.items():
    if colour in filled_colours:
      continue  # Skip already filled colours

    for row, col in positions:
      if (row, col) in placed_queens:
        continue  # Skip already placed queens

      if blocked_rows[row] or blocked_cols[col]:
        continue  # Skip blocked positions

      if _is_queen_placed_around(row, col, board, placed_queens):
        continue  # Skip if a queen is placed around

      # Place the queen
      board.place_queen(row, col)
      filled_colours.add(colour)
      placed_queens.add((row, col))

      blocked_rows[row] = True
      blocked_cols[col] = True

      # Recur
      result = _place_queens(board, sorted_compartments, filled_colours, 
                             placed_queens, blocked_rows, blocked_cols)
      
      if result:
        return result

      blocked_rows[row] = False
      blocked_cols[col] = False

      # Backtrack
      board.remove_queen(row, col)
      filled_colours.remove(colour)
      placed_queens.remove((row, col))

  return None

def _is_queen_placed_around(row: int, col: int, board: Board, placed_queens: set[tuple[int, int]]) -> bool:
  for r, c in placed_queens:
    if abs(row - r) <= 1 and abs(col - c) <= 1:
      return True
    
  return False