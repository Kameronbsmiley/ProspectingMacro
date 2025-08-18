import pyautogui
import time
import keyboard
from src.checking import *
from src.movement import *
import keyboard
import tkinter as tk
from tkinter import messagebox

dig_bar_width = 640
dig_bar_empty_hex = "#8c8c8c"
dig_bar_full_hex = "#f5df6d"

mouse_icon_hex = "#696969"  # Hex color for the mouse icon

dig_bar_top_left = (0, 0)
dig_bar_bottom_right = (0, 0)

dig_icon_location = (0, 0)

dig_speed_percent = 140 # Adjust this value based on your digging speed

def calibrate():
    """w
    Calibrate the position of the dig bar and luck text.
    """
    global dig_bar_top_left, dig_bar_bottom_right, dig_icon_location
    
    def get_mouse_position(prompt):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Calibration", prompt)
        pos = pyautogui.position()
        root.destroy()
        return pos

    # Prompt user for top left and bottom right corners
    dig_bar_top_left = get_mouse_position("Move your mouse to the TOP LEFT of the dig bar and press OK.")
    dig_bar_bottom_right = get_mouse_position("Move your mouse to the BOTTOM RIGHT of the dig bar and press OK.")

    # Calculate width and height
    width = dig_bar_bottom_right[0] - dig_bar_top_left[0]
    height = dig_bar_bottom_right[1] - dig_bar_top_left[1]

    # Take screenshot of the selected region
    screenshot = pyautogui.screenshot(region=(dig_bar_top_left[0], dig_bar_top_left[1], width, height))

    # Find exact top left and bottom right pixels of the dig bar by scanning for dig_bar_empty_hex
    def find_bar_edges(img, hex_color):
        pixels = img.load()
        w, h = img.size
        found_top_left = None
        found_bottom_right = None
        for y in range(h):
            for x in range(w):
                pixel = pixels[x, y]
                pixel_hex = '#{:02x}{:02x}{:02x}'.format(*pixel)
                if pixel_hex.lower() == hex_color.lower():
                    if not found_top_left:
                        found_top_left = (x, y)
                    found_bottom_right = (x, y)
        return found_top_left, found_bottom_right

    bar_top_left_rel, bar_bottom_right_rel = find_bar_edges(screenshot, dig_bar_empty_hex)

    if bar_top_left_rel and bar_bottom_right_rel:
        dig_bar_top_left = (dig_bar_top_left[0] + bar_top_left_rel[0], dig_bar_top_left[1] + bar_top_left_rel[1])
        dig_bar_bottom_right = (dig_bar_top_left[0] + (bar_bottom_right_rel[0] - bar_top_left_rel[0]),
                                dig_bar_top_left[1] + (bar_bottom_right_rel[1] - bar_top_left_rel[1]))

        # Move mouse to bottom right pixel and save screenshot of the bar itself
        bar_width = dig_bar_bottom_right[0] - dig_bar_top_left[0]
        bar_height = dig_bar_bottom_right[1] - dig_bar_top_left[1]
        bar_screenshot = pyautogui.screenshot(region=(dig_bar_top_left[0], dig_bar_top_left[1], bar_width, bar_height))
        bar_screenshot.save("calibrated_dig_bar.png")
    else:
        print("Could not find dig bar edges. Please recalibrate.")

    # Determine screenshot area below the dig bar to locate the dig icon
    bar_height = dig_bar_bottom_right[1] - dig_bar_top_left[1]
    search_top_left = (dig_bar_top_left[0], dig_bar_bottom_right[1] + bar_height)
    search_width = dig_bar_bottom_right[0] - dig_bar_top_left[0]
    search_height = bar_height

    search_screenshot = pyautogui.screenshot(region=(search_top_left[0], search_top_left[1], search_width, search_height))
    search_screenshot.save("dig_icon_search_area.png")
    found_dig_icon = None
    pixels = search_screenshot.load()
    for y in range(search_height):
        for x in range(search_width):
            pixel = pixels[x, y]
            pixel_hex = '#{:02x}{:02x}{:02x}'.format(*pixel)
            if pixel_hex.lower() == mouse_icon_hex.lower():
                found_dig_icon = (search_top_left[0] + x, search_top_left[1] + y)
                break
        if found_dig_icon:
            break

    if found_dig_icon:
        dig_icon_location = found_dig_icon
        print(f"Dig icon found at: {dig_icon_location}")
    else:
        print("Could not find dig icon pixel. Please recalibrate.")



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
        pyautogui.mouseDown(dig_icon_location[0], dig_icon_location[1], button='left')
        pyautogui.mouseUp(button='left')
    
    move_to_dig(dig_icon_location, mouse_icon_hex, start_digging)
        
# Uncomment the following line to start the panning process

if __name__ == "__main__":
    calibrate()
    print("Calibration complete. You can now start digging.")
    print("Dig bar rectangle:", dig_bar_top_left, dig_bar_bottom_right)
    print("Dig icon location:", dig_icon_location)
    start_digging()