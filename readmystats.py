from PIL import Image, ImageGrab
import numpy as np
from pynput import keyboard
from pynput.mouse import Button, Controller
import pyuac
import os
import sys
import time
import logging
from datetime import datetime
from statreader import StatReader
import tkinter as tk

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

logger = None
image_paths = dict()
all_coords = list()

def on_press(key):
    global all_coords
    #print(len(all_coords))
    if not all_coords:
        all_coords = read_coords()
        #print(len(all_coords))
        #logger.info(read_coords())
    mouse = Controller()
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == '~' or k == '`':  # keys of interest
        logger.info("Exiting!")
        exit()
    if k == '+':
        #TODO Add scalable resolutions/use OCR to identify where to click
        nikke_count = len(image_paths)
        if nikke_count > 0:
            nikke_count -= 1
        # moves to the visor
        print(all_coords)
        click_on(all_coords[0], mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths, nikke_count)
        click_on(all_coords[1], mouse=mouse)
        time.sleep(0.1)
        # chest
        click_on(all_coords[1], mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths, nikke_count)
        click_on(all_coords[2], mouse=mouse)
        time.sleep(0.1)
        #arm
        click_on(all_coords[2], mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths, nikke_count)
        click_on(all_coords[3], mouse=mouse)
        time.sleep(0.1)
        #boots
        click_on(all_coords[3], mouse=mouse)
        time.sleep(0.3)
        screenshot_script(image_paths, nikke_count)
        logger.info("Moving to new NIKKE")
        click_on(all_coords[4], mouse=mouse)
        click_on(all_coords[4], mouse=mouse)
        nikke_count = len(image_paths)
        logger.info("Creating a new NIKKE track")
        image_paths[nikke_count] = list()
    if k == '\\':
        nikke_count = len(image_paths)
        if nikke_count > 0:
            nikke_count -= 1
        screenshot_script(image_paths, nikke_count)
    #Move to next page/start new Nikke track
    if k == '.':
        #1507, 417 for 1920x1080
        click_on(all_coords[4], mouse=mouse)
        nikke_count = len(image_paths)
        logger.info("Moving to new NIKKE")
        if nikke_count > 0:
            if len(image_paths[nikke_count-1]) != 0:
                logger.info("Creating a new NIKKE track")
                image_paths[nikke_count] = list()
    if k == ']':
        coordinates = start_calibration()
        logger.info(coordinates)
        os.remove(".config")
        create_coord_file(coordinates)
        all_coords = read_coords()
        #Has to refocus window
        click_on(all_coords[0], mouse=mouse)
        time.sleep(0.3)
        click_on(all_coords[1], mouse=mouse)


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


def screenshot_script(image_paths, nikke_count):
    logger.info("Taking screenshot")
    if nikke_count in image_paths:
        x = len(image_paths[nikke_count])
    else:
        image_paths[nikke_count] = list()
        x = 0
    filename = "tmp_nk" + str(nikke_count) + "ct" + str(x) + ".png"
    screenshot_screen(filename)
    image_paths[nikke_count].append(filename)


def screenshot_screen(filename):
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    screenshot.close()

def create_coord_file(cord_dict=None):
    dir_list = os.listdir()
    if ".config" in dir_list:
        return
    f = open(".config", "x")
    if cord_dict and len(cord_dict) == 5:
        for coord in cord_dict:
            f.write(f"{coord[0]},{coord[1]}\n")
    else:
        #Default coordinates
        f.write("1324,616\n")
        f.write("1434,627\n")
        f.write("1329,704\n")
        f.write("1436,719\n")
        f.write("1507,450\n")
    f.close()

def read_coords():
    f = open(".config", "r")
    listed_cords = list()
    for line in f:
        line = line.replace("\n", "")
        cords = line.split(",")
        listed_cords.append((int(cords[0]), int(cords[1])))
    f.close()
    return listed_cords

def start_calibration():
    def on_click(event):
        coords.append((event.x, event.y))
        #logger.info(f"Captured coordinates: {event.x}, {event.y}")
        if len(coords) < 2:
            label.config(text=f"Point {len(coords)} captured for Visor. Please click on the Chest gear piece.")
        elif len(coords) < 3:
            label.config(text=f"Point {len(coords)} captured for Chest. Please click on the Arm gear piece.")
        elif len(coords) < 4:
            label.config(text=f"Point {len(coords)} captured for Arm. Please click on the Leg gear piece.")
        elif len(coords) < 5:
            label.config(text=f"Point {len(coords)} captured for Leg. Please click on the Right arrow to go to the next NIKKE.")
        else:
            label.config(text="Calibration complete. Closing window...")
            root.after(1000, root.destroy)

    def on_key_press(event):
        if event.keysym == "Escape":
            root.destroy()

    coords = []
    root = tk.Tk()
    root.title("Calibration")
    root.attributes("-fullscreen", True) 
    root.attributes("-alpha", 0.5) 
    root.attributes("-topmost", True) 
    root.configure(bg="gray") 

    label = tk.Label(root, text="To calibrate, please click on the Visor gear piece.\nPress ESC to exit.",
                     font=("Arial", 24), bg="gray", fg="white")
    label.pack(pady=20)

    root.bind("<Button-1>", on_click) 
    root.bind("<Escape>", on_key_press)

    root.mainloop()

    return coords

def start_up():
    def on_click(event):
         root.after(500, root.destroy)

    coords = []
    root = tk.Tk()
    root.title("Calibration")
    root.attributes("-fullscreen", True) 
    root.attributes("-alpha", 0.8) 
    root.attributes("-topmost", True) 
    root.configure(bg="black") 

    label = tk.Label(root, text="Thanks for using our tool. Here are the buttons you may need.\n"
                     "To start, we recommend pressing \"]\" to calibrate the tool.\n"
                     "Then you can press \"+\" to automatically capture each NIKKE's gear.\n"
                     "After you have captured what you have needed, press ~ or esc to stop the tool.\n"
                     "Check the folder this script is running in for a \"stats_*\" file that contains the data!\n"
                     "CLICK TO CLOSE THIS WINDOW <3",
                     font=("Arial", 24), bg="black", fg="white")
    label.pack(pady=20)

    root.bind("<Button-1>", on_click) 

    root.mainloop()

    return coords

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
        sys.exit()
    else:
        pass
    create_coord_file()
    logger = logging.getLogger("ReadMyStats")
    final_stats = dict()
    start_up()
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
    nikkepaths = dict()

    for path in image_paths:
        newpath = path.replace("tmp_nk", "")
        nikkeno = newpath.split("ct")[0]
        if nikkeno not in nikkepaths:
            nikkepaths[nikkeno] = list()
        nikkepaths[nikkeno].append(path)
    print(nikkepaths)
    #New statreader for every nikke
    sr = StatReader()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stats_{timestamp}.txt"
    stat_file = open(filename, "x")
    for nikke in nikkepaths:
        sr.ResetTotals()
        stat_file.write("NIKKE " + nikke + ": \n")
        gear_count = 1
        for path in nikkepaths[nikke]:
            stat_file.write("Gear " + str(gear_count) + ": \n")
            gear_count += 1
            part_stats = sr.ReadFileImage(path)
            #Prints each parts stats individually
            for stat in part_stats:
                if part_stats[stat] != 0:
                    stat_file.write(stat + ": " + str(part_stats[stat]) + "\n")
        stat_file.write("TOTAL STATS FOR NIKKE #" + str(nikke) + ": \n")
        for stat in sr.totals:
            if sr.totals[stat] != 0:
                stat_file.write(stat + ": " + str(sr.totals[stat]) + "\n")

    #logger.info("Press escape to leave")
    #with keyboard.Listener(on_press=on_release, on_release=on_release) as listener:
    #    listener.join()

    for path in image_paths:
        os.remove(path)
