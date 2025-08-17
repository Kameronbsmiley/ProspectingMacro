import time
import pyautogui
import pydirectinput
from . import checking

def move_to_water(dig_icon_location, mouse_hex, function_to_run):
    """
    Move the character to the water source.
    """
    while checking.get_current_state(dig_icon_location, mouse_hex) == "dig":
        pydirectinput.keyDown('down')
        time.sleep(0.5)
    pydirectinput.keyUp('down')
    function_to_run()
    
    

        
    
def move_to_dig(dig_icon_location, mouse_hex, function_to_run):
    """
    Move the character to the dig site.
    """
    print(dig_icon_location, mouse_hex)
    while checking.get_current_state(dig_icon_location, mouse_hex) == "pan":
        pydirectinput.keyDown('up')
        time.sleep(0.5)
    pydirectinput.keyUp('up')
    function_to_run()
    
    
    