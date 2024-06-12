from threading import Thread, Lock
from time import sleep
from enum import Enum

# Keyboard inputs and timing
from time import time
import pyautogui

# Custom librairies
from game.position import translate, getKey, getDirection
from a_star.path_finder import PathFinder


class BotState(Enum):
    COMPUTE_NEXT_MOVE = 0,
    WAIT_NEXT_BEAT = 1,
    MOVE = 2


class CryptBot:
    # Constants
    DURATION_BETWEEN_BEATS_IN_SECOND = 0.5

    # Thread properties
    stopped = True
    lock = None

    # Properties
    state = None
    game_map = None
    path = None
    last_beat_timestamp = None

    def __init__(self):
        # Create the thread lock object
        self.lock = Lock()
        self.map_lock = Lock()


        self.state = BotState.WAIT_NEXT_BEAT
        self.last_beat_timestamp = time()

      
    def update_game_map(self, game_map):
        self.lock.acquire()
        self.game_map = game_map
        self.lock.release()

    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    
    def stop(self):
        self.stopped = True


    def run(self):
        while not self.stopped:
            if self.state == BotState.COMPUTE_NEXT_MOVE:
                char_pos = self.game_map.get_character_position()
                stairs_pos = self.game_map.get_stairs_position()
                if char_pos is None or stairs_pos is None:
                    continue
                print("BotState.COMPUTE_NEXT_MOVE has positions")
                path_finder = PathFinder(self.game_map.get_width(), self.game_map.get_height())
                path_finder.set_start_end(char_pos, stairs_pos)
                path_finder.solve_astar()
                self.path = path_finder.get_shortest_path_node_iterator()

                self.lock.acquire()
                self.state = BotState.WAIT_NEXT_BEAT
                self.lock.release()

            elif self.state == BotState.WAIT_NEXT_BEAT:
                print("BotState.WAIT_NEXT_BEAT")
                if time() - self.last_beat_timestamp >= self.DURATION_BETWEEN_BEATS_IN_SECOND:
                    self.lock.acquire()
                    self.state = BotState.MOVE
                    self.lock.release()

            elif self.state == BotState.MOVE:
                print("BotState.MOVE")
                if self.path is not None:
                    next_node = self.path[1]
                    # Get the direction to go
                    new_position = (next_node.x, next_node.y)
                    choosen_direction = getDirection(char_pos, new_position)
                    # Press the key
                    if self.game_map.is_in_bounds(translate(char_pos, choosen_direction)):
                        pyautogui.press(getKey(choosen_direction))
                
                self.lock.acquire()
                self.state = BotState.COMPUTE_NEXT_MOVE
                self.last_beat_timestamp = time()
                self.lock.release()
            sleep(0.1)
