SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 16x16 Scaling
TILE_SIZE = 16
SCALE = 2
SCALED_TILE = TILE_SIZE * SCALE

# 32x32 Scaling Option Uncomment to use and comment out 16x16 
#TILE_SIZE = 32
#SCALE = 1  # Or set to 2 if you want 64x64 visual tiles
#SCALED_TILE = TILE_SIZE * SCALE

# Colours
BG_COLOURS = (40, 42, 54)
COLOURS = {
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),      # Bounce pad
    "red": (255, 0, 0),           # Hazard / Reset
    "start": (255, 255, 255),     # White
    "exit": (128, 0, 128)         # Purple 
}