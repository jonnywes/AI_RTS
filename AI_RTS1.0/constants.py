# constants.py

# ==========================================
# UI & DISPLAY SETTINGS
# ==========================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30

# Map Panel Dimensions (Left side)
MAP_WIDTH = 800
MAP_HEIGHT = 720

# Terminal Panel Dimensions (Right side)
TERMINAL_WIDTH = SCREEN_WIDTH - MAP_WIDTH
TERMINAL_HEIGHT = 720
INPUT_BOX_HEIGHT = 200 # Height for the paste/input area

# Colors (RGB)
COLOR_BG_MAP = (30, 30, 30)
COLOR_BG_TERMINAL = (15, 15, 15)
COLOR_TEXT = (200, 200, 200)
COLOR_HIVE = (200, 150, 50)
COLOR_INPUT_BG = (40, 40, 40)
COLOR_HIGHLIGHT = (100, 200, 100)

# ==========================================
# GAMEPLAY MECHANICS & BALANCING
# ==========================================

# Starting Stats
STARTING_FOOD = 100
STARTING_WORKERS = 5
STARTING_WARRIORS = 0

# Food Consumption (Start of Turn)
UPKEEP_QUEEN = 5
UPKEEP_WARRIOR = 1
UPKEEP_WORKER = 0 # Assuming workers sustain themselves, adjust if needed

# Food Generation (End of Turn)
GATHER_RATE_BASE = 2
GATHER_RATE_BOOSTED = 4 # Modifier for "Focus on gathering food"

# Production Costs (To be deducted when spawning)
COST_WORKER = 10
COST_WARRIOR = 15
COST_QUEEN = 50 # High cost to establish a new Hive

# ==========================================
# AI / PARSER CONSTANTS
# ==========================================

# Expected Target strings
TARGET_QUEEN = "QUEEN"

# Valid Action Strings (Must exactly match expected LLM output)
ACTION_GATHER_FOOD = "Focus on gathering food"
ACTION_PRODUCE_WORKERS = "Produce Workers"
ACTION_PRODUCE_WARRIORS = "Produce Warriors"
ACTION_PRODUCE_QUEEN = "Produce a new queen"

# For validation purposes
VALID_ACTIONS = [
    ACTION_GATHER_FOOD,
    ACTION_PRODUCE_WORKERS,
    ACTION_PRODUCE_WARRIORS,
    ACTION_PRODUCE_QUEEN
]
