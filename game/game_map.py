from enum import Enum
from window_capture import MINIMAP_WIDTH, MINIMAP_HEIGHT

class CellType(Enum):
    EMPTY = " "
    CHARACTER = "C"
    DOWNSTAIRS = "D"
    WALL = "W"
    ENEMY = "E"

CELL_TO_STR = {}
CELL_TO_STR[CellType.EMPTY] = ' '
CELL_TO_STR[CellType.CHARACTER] = 'Ϙ'
CELL_TO_STR[CellType.DOWNSTAIRS] = 'X'      # Ϟ
CELL_TO_STR[CellType.WALL] = 'Π'
CELL_TO_STR[CellType.ENEMY] = 'O'           # Ω

FULLWINDOW_GAME_MAP_WIDTH_IN_CELL = 27
FULLWINDOW_GAME_MAP_HEIGHT_IN_CELL = 14

MINIMAP_CELL_SIZE = 6
MINIMAP_GAME_MAP_WIDTH_IN_CELL = int(MINIMAP_WIDTH / MINIMAP_CELL_SIZE)
MINIMAP_GAME_MAP_HEIGHT_IN_CELL = int(MINIMAP_HEIGHT / MINIMAP_CELL_SIZE)

class GameMap:
    width = 0
    height = 0
    board = None
    character_position = None
    stairs_position = None

    def __init__(self, width=FULLWINDOW_GAME_MAP_WIDTH_IN_CELL, height=FULLWINDOW_GAME_MAP_HEIGHT_IN_CELL):
        self.width = width
        self.height = height
        self.clear_cells()

    
    def __str__(self):
        #result = "(" + str(self.width) + "," + str(self.height) + ")\n"
        result = "  "
        for _ in range(6):
            result += " "
        result += "⑤"
        for _ in range(4):
            result += " "
        result += "⑩"
        for _ in range(4):
            result += " "
        result += "⑮"
        for _ in range(4):
            result += " "
        result += "⑳"
        for _ in range(4):
            result += " "
        result += "㏸\n"
        result += "  +"
        for _ in range(self.width):
            result += "-"
        result += "+\n"
        for y in range(self.height):
            result += "{:02d}".format(y) + "|"
            for x in range(self.width):
                result += CELL_TO_STR[self.board[y][x]]
            result += "|\n"
        result += "  +"
        for _ in range(self.width):
            result += "-"
        result += "+"
        return result


    def get_width(self):
        return self.width

    
    def get_height(self):
        return self.height


    # Return the CellType at the position, a (x, y) tuple
    def get_cell(self, position):
        return self.board[position[1]][position[0]]


    def get_character_position(self):
        return self.character_position


    def get_stairs_position(self):
        return self.stairs_position


    def set_cell(self, position, CellType):
        self.board[position[1]][position[0]] = CellType


    # Return true if the position in the bounds of the board
    def is_in_bounds(self, position):
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height
    

    '''Convert the position of a pixel in a game screenshot to a CellType position representing the game
    @param pixel_position a (x, y) tuple
    @param game_sizes a (width, height) tuple
    '''
    def convert_pixel_position_to_cell_position(self, pixel_position, game_resolution):
        cell_width = int(game_resolution[0] / self.width)
        cell_height = int(game_resolution[1] / self.height)
        x_cell = int(pixel_position[0] / cell_width)
        y_cell = int(pixel_position[1] / cell_height)
        return (x_cell, y_cell) 

    # Set the content of all cells at CellType.EMPTY
    def clear_cells(self):
        self.character_position = None
        # self.board = [[CellType.EMPTY] * self.width] * self.height
        self.board = []
        for y in range(self.height):
            self.board.append([])
            for _ in range(self.width):
                self.board[y].append(CellType.EMPTY)

    '''Set the CellType with cell_content at the centers' positions
    @param centers, a list of position (x, y) tuple, x and y in pixel of the screen
    @param cell_content, a element of the CellType enum
    @param window_capture, the window_capture instance from which the centers have been found
    '''
    def update_cells(self, centers, cell_content, window_capture):
        for center in centers:
            game_resolution = window_capture.get_game_resolution()
            cell_pos = self.convert_pixel_position_to_cell_position(center, game_resolution)
            self.set_cell(cell_pos, cell_content)
            if cell_content == CellType.CHARACTER:
                self.character_position = cell_pos
            if cell_content == CellType.DOWNSTAIRS:
                self.stairs_position = cell_pos
