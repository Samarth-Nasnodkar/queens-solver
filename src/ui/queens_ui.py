import pygame

from utils.board import Board
from solver.queens_solver import queens_solver
from utils.enums.board_marker import BoardMarker


class QueensUI:
  """
  A Pygame UI class to display a 480x480 screen with a centered 8x8 board.

  To the left of the board, display 8 mini squares representing the colors.
  Place these squares in a vertical column.
  These will act like buttons to place those colors on the squares
  on the board clicked next.
  """

  BOARD_SIZE = 8
  SQUARE_SIZE = 48
  BOARD_PIXEL_SIZE = BOARD_SIZE * SQUARE_SIZE
  COLOR_BUTTON_SIZE = 32
  COLOR_BUTTON_MARGIN = 8
  COLOR_BUTTON_AREA_WIDTH = COLOR_BUTTON_SIZE + 2 * COLOR_BUTTON_MARGIN

  COLOURS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 0, 128),  # Purple
    (255, 165, 0),  # Orange
  ]

  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((480, 480))
    self.clock = pygame.time.Clock()
    self.board = Board(self.BOARD_SIZE)
    self.running = True
    self.selected_color = 0  # Index in COLORS

    # Calculate board position to center it with color buttons on the left
    total_width = self.COLOR_BUTTON_AREA_WIDTH + self.BOARD_PIXEL_SIZE
    self.board_origin_x = self.COLOR_BUTTON_AREA_WIDTH + (480 - total_width) // 2
    self.board_origin_y = (480 - self.BOARD_PIXEL_SIZE) // 2

  def run(self):
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.handle_mouse(event.pos)

      self.screen.fill((255, 255, 255))
      self.draw_color_buttons()
      self.draw_board()
      pygame.display.flip()
      self.clock.tick(60)

    pygame.quit()

  def draw_color_buttons(self):
    for i, color in enumerate(self.COLOURS):
      x = self.COLOR_BUTTON_MARGIN
      y = self.COLOR_BUTTON_MARGIN + i * (self.COLOR_BUTTON_SIZE + self.COLOR_BUTTON_MARGIN)
      rect = pygame.Rect(x, y, self.COLOR_BUTTON_SIZE, self.COLOR_BUTTON_SIZE)
      pygame.draw.rect(self.screen, color, rect)
      if i == self.selected_color:
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
      else:
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

  def draw_board(self):
    for row in range(self.BOARD_SIZE):
      for col in range(self.BOARD_SIZE):
        x = self.board_origin_x + col * self.SQUARE_SIZE
        y = self.board_origin_y + row * self.SQUARE_SIZE
        rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
        color = self.COLOURS[self.board.board[row][col][0]]
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        # Draw color if set
        square_color = self.board.get_color(row, col) if hasattr(self.board, "get_color") else None
        if square_color is not None:
          pygame.draw.circle(self.screen, self.COLOURS[square_color],
             rect.center, self.SQUARE_SIZE // 3)
        # Draw marker if set
        marker = self.board.board[row][col][1]
        if marker is not None and marker != BoardMarker.EMPTY:
          font = pygame.font.SysFont(None, 24)
          marker_text = 'Q' if marker == BoardMarker.QUEEN else ''
          text = font.render(marker_text, True, (0, 0, 0))
          text_rect = text.get_rect(center=rect.center)
          self.screen.blit(text, text_rect)

  def handle_mouse(self, pos):
    x, y = pos
    # Check color button clicks
    for i in range(len(self.COLOURS)):
      bx = self.COLOR_BUTTON_MARGIN
      by = self.COLOR_BUTTON_MARGIN + i * (self.COLOR_BUTTON_SIZE + self.COLOR_BUTTON_MARGIN)
      rect = pygame.Rect(bx, by, self.COLOR_BUTTON_SIZE, self.COLOR_BUTTON_SIZE)
      if rect.collidepoint(x, y):
        self.selected_color = i
        return

    # Check solve button click
    solve_btn_x = self.COLOR_BUTTON_MARGIN
    solve_btn_y = self.COLOR_BUTTON_MARGIN + len(self.COLOURS) * (self.COLOR_BUTTON_SIZE + self.COLOR_BUTTON_MARGIN)
    solve_btn_rect = pygame.Rect(solve_btn_x, solve_btn_y, self.COLOR_BUTTON_SIZE, self.COLOR_BUTTON_SIZE)
    if solve_btn_rect.collidepoint(x, y):
      # Import here to avoid circular import at top
      solution = queens_solver(self.board)
      if solution:
        self.board = solution
      return

    # Check board clicks
    bx = self.board_origin_x
    by = self.board_origin_y
    if bx <= x < bx + self.BOARD_PIXEL_SIZE and by <= y < by + self.BOARD_PIXEL_SIZE:
      col = (x - bx) // self.SQUARE_SIZE
      row = (y - by) // self.SQUARE_SIZE
      self.board.update_cell_colour(row, col, self.selected_color)
      self.draw_board()

  def draw_color_buttons(self):
    for i, color in enumerate(self.COLOURS):
      x = self.COLOR_BUTTON_MARGIN
      y = self.COLOR_BUTTON_MARGIN + i * (self.COLOR_BUTTON_SIZE + self.COLOR_BUTTON_MARGIN)
      rect = pygame.Rect(x, y, self.COLOR_BUTTON_SIZE, self.COLOR_BUTTON_SIZE)
      pygame.draw.rect(self.screen, color, rect)
      if i == self.selected_color:
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
      else:
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
    # Draw solve button
    solve_btn_x = self.COLOR_BUTTON_MARGIN
    solve_btn_y = self.COLOR_BUTTON_MARGIN + len(self.COLOURS) * (self.COLOR_BUTTON_SIZE + self.COLOR_BUTTON_MARGIN)
    solve_btn_rect = pygame.Rect(solve_btn_x, solve_btn_y, self.COLOR_BUTTON_SIZE, self.COLOR_BUTTON_SIZE)
    pygame.draw.rect(self.screen, (200, 200, 200), solve_btn_rect)
    pygame.draw.rect(self.screen, (0, 0, 0), solve_btn_rect, 2)
    font = pygame.font.SysFont(None, 18)
    text = font.render("Solve", True, (0, 0, 0))
    text_rect = text.get_rect(center=solve_btn_rect.center)
    self.screen.blit(text, text_rect)
