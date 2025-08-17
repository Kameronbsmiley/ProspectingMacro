import pyautogui


def get_current_state(dig_icon_location, mouse_hex):
    """
    See if you're prompted to dig or pan.
    """
    screenshot = pyautogui.screenshot()
    pixel = screenshot.getpixel((dig_icon_location[0], dig_icon_location[1]))
    hex_color = '#{:02x}{:02x}{:02x}'.format(*pixel)
    
    print(hex_color, mouse_hex)
    
    if hex_color.lower() == mouse_hex.lower():
        print("Dig Icon Shown.")
        return "dig"
    else:
        print("Panning Icon Shown.")
        return "pan"

