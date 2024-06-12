from time import time

# Computer vision: https://docs.opencv.org/4.5.3/index.html
import cv2 as cv

# Custom librairies
from window_capture import WindowCapture
from computer_vision.vision import Vision
from computer_vision.detection import Detection
from game.game_map import CellType, GameMap, MINIMAP_GAME_MAP_WIDTH_IN_CELL, MINIMAP_GAME_MAP_HEIGHT_IN_CELL
from game.bot import CryptBot

# Constants
BLUE_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (0, 0, 255)
WHITE_COLOR = (255, 255, 255)

DEBUG = True


def main():
    # Classes initialization
    wincap = WindowCapture("Crypt of the NecroDancer")
    detector = Detection()
    game_map = GameMap(MINIMAP_GAME_MAP_WIDTH_IN_CELL, MINIMAP_GAME_MAP_HEIGHT_IN_CELL)
    bot = CryptBot()

    wincap.start()
    detector.start()
    bot.start()

    begin_loop_time = time()
    while(True):
        if wincap.screenshot is None:
            continue
        
        detector.update(wincap.screenshot)

        # Update the game board
        ch_centers = Vision.get_centers_of_rectangles(detector.character_rectangles)
        print("ch_center", ch_centers)
        ds_centers = Vision.get_centers_of_rectangles(detector.downstairs_rectangles)
        print("ds_center", ds_centers)
        game_map.clear_cells()
        game_map.update_cells(ch_centers, CellType.CHARACTER, wincap)
        game_map.update_cells(ds_centers, CellType.DOWNSTAIRS, wincap)

        bot.update_game_map(game_map)

        if DEBUG:
            # DEBUG
            # print("\nGame state")
            # print(game_map)
            # Draw the detection's result onto the original image
            output_image = Vision.draw_rectangles(wincap.screenshot, detector.downstairs_rectangles)
            output_image = Vision.draw_crosshairs(wincap.screenshot, ds_centers)
            output_image = Vision.draw_rectangles(wincap.screenshot, detector.character_rectangles, RED_COLOR)
            output_image = Vision.draw_crosshairs(wincap.screenshot, ch_centers)
            # output_image = Vision.draw_rectangles(wincap.screenshot, detector.wall_rectangles, WHITE_COLOR)

            # Display the processed image
            #cv.imshow("HSV vision", processed_image)
            # Resize the debug window
            # https://answers.opencv.org/question/84985/resizing-the-output-window-of-imshow-function/
            cv.namedWindow("Matches", cv.WINDOW_NORMAL)
            w, h = wincap.get_game_resolution()
            cv.resizeWindow('Matches', w, h)
            cv.imshow("Matches", output_image)

            # Debug the loop rate
            print("FPS {:.2f}".format(1 / (time() - begin_loop_time)))
            begin_loop_time = time()

        # Press 'q' to exit the program
        if cv.waitKey(1) == ord('q'):
            detector.stop()
            wincap.stop()
            bot.stop()
            cv.destroyAllWindows()
            break

    print("End of program")

if __name__ == "__main__":
    main()