import easyocr
from PIL import Image, ImageGrab
import numpy as np
from pynput import keyboard
from pynput.mouse import Button, Controller
import pyuac
import os
import sys
import time
import logging

# Configure the logging
logging.basicConfig(
    level=logging.INFO,  # Set the minimum logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=
    [
        #logging.FileHandler("log.txt"), # Log to a file
        logging.StreamHandler() # Log to console
    ]
)

# All possible stat rolls for
possible_values = {
    "Increase Element Damage Dealt": [9.54, 10.94, 12.34, 13.75, 15.15, 16.55, 17.95, 19.35, 20.75, 22.15, 23.56, 24.96, 26.36, 27.76, 29.16],
    "Increase Max Ammunition Capacity": [27.84, 31.95, 36.06, 40.17, 44.28, 48.39, 52.50, 56.60, 60.71, 64.82, 68.93, 73.04, 77.15, 81.26, 85.37],
    "Increase Critical Damage": [6.64, 7.62, 8.60, 9.58, 10.56, 11.54, 12.52, 13.50, 14.48, 15.46, 16.44, 17.42, 18.40, 19.38, 20.36],
    "Increase Critical Rate": [2.30, 2.64, 2.98, 3.32, 3.66, 4.00, 4.35, 4.69, 5.03, 5.37, 5.71, 6.05, 6.39, 6.73, 7.07],
    "Increase Charge Damage": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
    "Increase Charge Speed": [1.98, 2.28, 2.57, 2.86, 3.16, 3.45, 3.75, 4.04, 4.33, 4.63, 4.92, 5.21, 5.51, 5.80, 6.09],
    "Increase ATK": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
    "Increase Hit Rate": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
    "Increase DEF": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
}

reader = None  # easyOCR reader
logger = None


# IMAGE_PATH => Path to the image
def alter_image(IMAGE_PATH="image.png"):
    img = Image.open(IMAGE_PATH).convert("RGB")
    newsize = (1920, 1080)
    img = img.resize(newsize)

    img.crop((700, 715, 1156, 860)).save(IMAGE_PATH)


def read_image(path="tmp_file.png"):
    result = reader.readtext(path)
    result_string = ""
    for detection in result:
        result_string += detection[1] + " "
    return result_string


def evaluate_result(result_string, final_stats):
    stat_lines = result_string.split("%")
    for stat_line in stat_lines:
        stat_split = stat_line.rsplit(" ", 1)
        if stat_split[0] in possible_values:
            if (
                stat_split[1].lower() == "il.m1"
                or stat_split[1].lower() == "ii.ii"
                or stat_split[1].lower() == "ll.ll"
                or stat_split[1].lower() == "ii.ll"
                or stat_split[1].lower() == "ll.ii"
            ):
                stat_split[1] = "11.11"
            if stat_split[1] in possible_values[stat_split[0]]:
                final_stats[stat_split[0]] += float(stat_split[1])
            else:
                if str(float(stat_split[1]) / 100) in possible_values[stat_split[0]]:
                    final_stats[stat_split[0]] += float(stat_split[1]) / 100
                else:
                    logger.error("Line: " + stat_line)
        else:
            if not stat_split[0].isspace() and stat_split[0]:
                logger.warning("Unexpected attribute: ")
                logger.warning(stat_split)
                logger.warning("You can manually input this to accurately represent your equipment.")


image_paths = list()


def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if k == '~' or k == '`':  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        logger.info("Exiting!")
        exit()
    if k == '+':
        """The current pointer position is (1324, 616)
        The current pointer position is (1434, 627)
        The current pointer position is (1329, 704)
        The current pointer position is (1436, 719)"""
        mouse = Controller()
        # moves to the first equipment
        click_on((1324, 616), mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths)
        click_on((1434, 627), mouse=mouse)
        time.sleep(0.1)
        click_on((1434, 627), mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths)
        click_on((1329, 704), mouse=mouse)
        time.sleep(0.1)
        click_on((1329, 704), mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths)
        click_on((1436, 719), mouse=mouse)
        time.sleep(0.1)
        click_on((1436, 719), mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths)
    if k == '\\':
        screenshot_script(image_paths)


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        exit()


def click_on(position, mouse):
    mouse.position = position
    time.sleep(0.05)
    mouse.press(Button.left)
    time.sleep(0.025)
    mouse.release(Button.left)


def screenshot_script(image_paths):
    logger.info("Taking screenshot")
    x = len(image_paths) + 1
    filename = "tmp" + str(x) + ".png"
    screenshot_screen(filename)
    alter_image(filename)
    image_paths.append(filename)


def screenshot_screen(filename):
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    screenshot.close()


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
        sys.exit()
    else:
        pass
    reader = easyocr.Reader(["en"])
    logger = logging.getLogger("ReadMyStats")

    final_stats = dict()
    for key in possible_values:
        final_stats[key] = 0

    logger.info("Awaiting inputs!")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # After collecting images, do the reading all at once
    dir_list = os.listdir()

    image_paths = list()
    for files in dir_list:
        if files.startswith("tmp"):
            image_paths.append(files)
    for path in image_paths:
        result = read_image(path)
        evaluate_result(result_string=result, final_stats=final_stats)
    logger.info("TOTAL STATS:")
    for stat in final_stats:
        if final_stats[stat] != 0:
            logger.info(stat + ": " + str(final_stats[stat]))

    logger.info("Press escape to leave")
    with keyboard.Listener(on_press=on_release, on_release=on_release) as listener:
        listener.join()

    for path in image_paths:
        os.remove(path)
