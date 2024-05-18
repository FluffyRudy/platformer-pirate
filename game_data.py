from settings import SCREEN_WIDTH, SCREEN_HEIGHT

AVILABLE = 1
NOT_AVILABLE = 0
NODE_WIDTH = 100
NODE_HEIGHT = 100
NUM_LEVELS = 6

offset =  (SCREEN_WIDTH - NODE_WIDTH * NUM_LEVELS) // 6
start_x = (SCREEN_WIDTH - NODE_WIDTH * NUM_LEVELS) // 6

levels = {
    0: {'node_pos': (start_x + offset, 400), 'content': 'level 0', 'unlock': 1},
    1: {'node_pos': (start_x + offset * 2, 400), 'content': 'level 1', 'unlock': 2},
    2: {'node_pos': (start_x + offset * 3, 400), 'content': 'level 2', 'unlock': 3},
    3: {'node_pos': (start_x + offset * 4, 400), 'content': 'level 3', 'unlock': 4},
    4: {'node_pos': (start_x + offset *  5, 400), 'content': 'level 4', 'unlock': 5},
    5: {'node_pos': (start_x + offset * 6, 400), 'content': 'level 5', 'unlock': 5},
} 