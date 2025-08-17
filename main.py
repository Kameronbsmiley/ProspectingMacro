import pyautogui
import time

from src.checking import *
from src.movement import *


dig_bar_width = 640
dig_bar_empty_hex = "#8c8c8c"
dig_bar_full_hex = "#f5df6d"

mouse_icon_hex = "#696969"  # Hex color for the mouse icon

dig_bar_top_left = (0, 0)
dig_bar_bottom_right = (0, 0)

dig_icon_location = (0, 0)
pan_icon_location = (0, 0)

dig_speed_percent = 140 # Adjust this value based on your digging speed

def calibrate():
    """
    Calibrate the position of the dig bar and luck text.
    """
    print("Please click the top-left corner of the region to calibrate.")
    top_left = pyautogui.position()
    pyautogui.alert("Move mosue around top left of dig bar and hit enter to continue")
    top_left = pyautogui.position()

    print("Now click the bottom-right corner of the region to calibrate.")
    pyautogui.alert("Move mouse around bottom right of dig bar and hit enter to continue")
    bottom_right = pyautogui.position()

    region = (top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)
    screenshot = pyautogui.screenshot(region=region)
    width, height = screenshot.size
    screenshot.save("calibration_screenshot.png")
    found = False
    for y in range(height):
        for x in range(width):
            pixel = screenshot.getpixel((x, y))
            hex_color = '#{:02x}{:02x}{:02x}'.format(*pixel)
            if hex_color.lower() == "#8c8c8c".lower():
                screen_x = top_left.x + x
                screen_y = top_left.y + y
                pyautogui.moveTo(screen_x, screen_y)
                pyautogui.click()
                print(f"Found color at ({screen_x}, {screen_y})")
                
                global dig_bar_top_left, dig_bar_bottom_right, dig_icon_location, pan_icon_location
                
                dig_bar_top_left = (screen_x, screen_y) # Update the top-left corner
                dig_bar_bottom_right = (dig_bar_top_left[0] + (dig_bar_width - 1), dig_bar_top_left[1] + 51)
                
                dig_icon_location = (dig_bar_top_left[0] + 156, dig_bar_top_left[1] + 139)  # Adjusted for collect icon
                pan_icon_location = (dig_bar_top_left[0] + 256, dig_bar_top_left[1] + 139)  # Adjusted for pan icon
                
                print(dig_icon_location, pan_icon_location)
                pyautogui.moveTo(dig_icon_location)  # Move mouse out of the way
                found = True
                
                break
        if found:
            break
    if not found:
        print("Specified color not found in the selected region.")

    return dig_bar_top_left, dig_bar_bottom_right


def start_digging():
    hold_time = (-0.015 * dig_speed_percent) + 2.5  # Linear formula to determine hold time based on dig speed
    
    can_dig = True
    
    """
    Start the digging process.
    """
    print("Starting digging process...")
    while can_dig:
        # Check if the dig bar is full
        print("Digbar top left:", dig_bar_top_left)
        screenshot = pyautogui.screenshot(region=(dig_bar_top_left[0], dig_bar_top_left[1], dig_bar_width, 52))
        screenshot.save("dig_bar_screenshot.png")
       
        pixel = screenshot.getpixel((screenshot.width - 1, screenshot.height - 1))
        hex_color = '#{:02x}{:02x}{:02x}'.format(*pixel)
        if hex_color.lower() == dig_bar_full_hex.lower():
            print("Dig bar is full. Stopping digging.")
            can_dig = False
            break
        # Simulate digging action
        pyautogui.mouseDown(dig_bar_top_left[0] + dig_bar_width // 2, dig_bar_top_left[1] + 25, button='left')
        time.sleep(hold_time)  # hold_time should be defined elsewhere (in seconds)
        pyautogui.mouseUp(button='left')
        time.sleep(0.5)  # Adjust sleep time as needed
    move_to_water(dig_icon_location, mouse_icon_hex, start_panning)
    

def start_panning():
    """
    This will be called when the player is prompted to pan.
    """
    
    # Continuously take new screenshots and check if the dig bar is empty
    while True:
        screenshot = pyautogui.screenshot(region=(dig_bar_top_left[0], dig_bar_top_left[1], dig_bar_width, 52))
        pixel = screenshot.getpixel((0, 0))
        hex_color = '#{:02x}{:02x}{:02x}'.format(*pixel)
        if hex_color.lower() == dig_bar_empty_hex.lower():
            print("Dig bar is empty. Stopping panning.")
            break

        # Simulate panning action
        pyautogui.mouseDown(pan_icon_location[0], pan_icon_location[1], button='left')
        pyautogui.mouseUp(button='left')
        
    move_to_dig(dig_icon_location, mouse_icon_hex, start_digging)
        
# Uncomment the following line to start the panning process

if __name__ == "__main__":
    calibrate()
    start_digging()

