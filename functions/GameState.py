from enum import Enum

class GameState(Enum):
    MAIN_MENU = 0
    GAME_START = 1
    SHOP = 2
    SETTINGS = 3
    LEADERBOARD = 4
    SCORE_INPUT = 5