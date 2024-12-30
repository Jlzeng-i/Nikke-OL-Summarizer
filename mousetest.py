from pynput import mouse
from pynput.mouse import Button, Controller
import pyuac
import sys
mice = Controller()
cool_list = list()
def on_click(x, y, button, pressed):
    print('The current pointer position is {0}'.format(
    mice.position))
    cool_list.append(0)
def on_scroll(x, y, dx, dy):
    exit()

if __name__ == "__main__":
    #if not pyuac.isUserAdmin():
    #    print("Re-launching as admin!")
    #    pyuac.runAsAdmin()
    #    sys.exit()
    #else:
    #    pass

    with mouse.Listener(
            on_move=None,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()

    while len(cool_list < 10):
        pass
