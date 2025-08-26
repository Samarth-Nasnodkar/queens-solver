from enum import Enum

class BoardEvent(Enum):
  QUEEN_PLACED = "queen_placed"
  BLOCKER_PLACED = "blocker_placed"
  MARKER_REMOVED = "marker_removed"
  COLOUR_UPDATED = "colour_updated"