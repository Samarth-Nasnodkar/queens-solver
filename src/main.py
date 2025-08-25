from solver.queens_solver import queens_solver
from utils.board import Board

if __name__ == '__main__':
  # Create a board instance and call the solver
  board = Board(size=8)
  tbl = [
    '01111122',
    '01311222',
    '11317222',
    '11117242',
    '15112242',
    '15162222',
    '11162222',
    '11222222'
  ]

  for r in range(8):
    for c, char in enumerate(tbl[r]):
      board.set_colour(r, c, int(tbl[r][c]))

  solution = queens_solver(board)
  for row in solution.board:
    print(" ".join(str(item[1]) for item in row))