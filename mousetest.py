from pynput.mouse import Button, Controller
import pyuac
import sys

if not pyuac.isUserAdmin():
    print("Re-launching as admin!")
    pyuac.runAsAdmin()
    sys.exit()
else:        
    pass
mouse = Controller()
mouse.position = (1650, 766)
mouse.press(Button.left)
mouse.release(Button.left)
mouse.position = (1790, 780)
mouse.press(Button.left)
mouse.release(Button.left)