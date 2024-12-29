import easyocr
from PIL import Image, ImageGrab 
import numpy as np       
from pynput import keyboard
import pyuac
import os
import sys


#Load all possible values for every substat

possible_values = dict()
with open("possiblevalues.txt") as file:
    for line in file:
        raw_split = line.split("\t")
        raw_split[-1] = raw_split[-1].replace("\n", "")
        possible_values[raw_split[0]] = raw_split[1:]
reader = easyocr.Reader(['en'])
# IMAGE_PATH => Path to the image 
def alter_image(IMAGE_PATH="image.png"):
    img = Image.open(IMAGE_PATH).convert('RGB') 
    newsize = (1920, 1080)
    img = img.resize(newsize)

    img.crop((700, 750, 1156, 860)).save(IMAGE_PATH)

#uncomment to load new image
#alter_image("image.png") 

def read_image(path="tmp_file.png"):
    result = reader.readtext(path)
    result_string = ""
    for detection in result:
        result_string += detection[1] + " "
    return result_string

def evaluate_result(result_string, final_stats):
    result_string = result_string.replace("Effect not obtained ", "")
    stat_lines = result_string.split("% ")
    for stat_line in stat_lines:
        stat_split = stat_line.rsplit(" ", 1)
        if stat_split[0] in possible_values:
            if stat_split[1].lower() == "il.m1" or stat_split[1].lower() == "ii.ii" or stat_split[1].lower() == "ll.ll" or stat_split[1].lower() == "ii.ll" or stat_split[1].lower() == "ll.ii":
                    stat_split[1] = "11.11"
            if stat_split[1] in possible_values[stat_split[0]]:
                final_stats[stat_split[0]] += float(stat_split[1])
            else:
                if str(float(stat_split[1])/100) in possible_values[stat_split[0]]:
                    final_stats[stat_split[0]] += float(stat_split[1])/100
                else:
                    print("ERROR in line: " + stat_line)
        else:
            if not stat_split[0].isspace() and stat_split[0]:
                print("Unexpected attribute: ")
                print(stat_split)
                print("You can manually input this to accurately represent your equipment.")

image_paths = list()
def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == '~':  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Exiting!')
        exit()
    if k == '\\':
        print('Time to run screenshot script!')
        x = len(image_paths) + 1
        filename = "tmp" + str(x) + ".png"
        screenshot_screen(filename)
        alter_image(filename) 
        image_paths.append(filename)

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        exit()

def screenshot_screen(filename):
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    screenshot.close()

if __name__=="__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
        sys.exit()
    else:        
        pass
    final_stats = dict()
    for key in possible_values:
        final_stats[key] = 0

    print("Awaiting inputs!")
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    
    #After collecting images, do the reading all at once
    dir_list = os.listdir()
    #print(dir_list)
    image_paths = list()
    for files in dir_list:
        if files.startswith("tmp"):
            image_paths.append(files)
    for path in image_paths:
        result = read_image(path)
        evaluate_result(result_string=result, final_stats=final_stats)
        os.remove(path) 
    print("TOTAL STATS:")
    for stat in final_stats:
        if final_stats[stat] != 0:
            print(stat + ": " + str(final_stats[stat]))
    
    print("Press escape to leave")
    with keyboard.Listener(
            on_press=on_release,
            on_release=on_release) as listener:
        listener.join()