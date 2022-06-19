import pygame
from win32api import GetSystemMetrics


# Color
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (244, 226, 198)
LIGHT_SLATE_GRAY = (119, 136, 153)
BLUE = (0, 0, 255)
GREEN = (124, 252, 0)
MAGENTA = (255, 0, 144)
YELLOW = (255, 255, 0)

# Screen resolution
WIDTH = GetSystemMetrics(0) // 3
HEIGHT = GetSystemMetrics(1) // 3

# Grid size
RATIO = 14
NUM_OF_GRID = 8
PIX_GRID_SIZE = HEIGHT / RATIO

CENTER_OF_SCREEN_X = WIDTH / 2
TOP_LEFT_BLOCK_X = CENTER_OF_SCREEN_X - PIX_GRID_SIZE * (NUM_OF_GRID / 2)
TOP_LEFT_BLOCK_Y = HEIGHT / RATIO * ((RATIO - NUM_OF_GRID) / 2) - NUM_OF_GRID

TOP_LEFT_BLOCK_POS = [TOP_LEFT_BLOCK_X, TOP_LEFT_BLOCK_Y]

BLOCK_SIZE = PIX_GRID_SIZE / 10 * 8
WIDTH_HEIGHT = (BLOCK_SIZE, BLOCK_SIZE)

# Pygame Frame
FRAME = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder")
FRAME.fill(BEIGE)

# Logic table Flag
EMPTY_FLAG = 0
WALL_FLAG = 1
SRC_FLAG = 2
DST_FLAG = 3

# Invalid flags
INVALID_FLAG = -1
INVALID_BLOCK_SELECTED_FLAG = [-1, -1]
INVALID_INDEX = [-1, -1]
NO_VALID_ROUTE_FLAG = "-1"

# Block colors
SRC_BLOCK_COLOR = RED
DST_BLOCK_COLOR = GREEN
EMPTY_BLOCK_COLOR = WHITE
WALL_BLOCK_COLOR = LIGHT_SLATE_GRAY
SEARCH_BLOCK_COLOR = BLUE
SUCCESSFUL_ROUTE_COLOR = YELLOW