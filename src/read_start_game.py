from read_text import detect_text_in_region

def in_starting_hand(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in in_starting_hand")
        return None

    rel_x1, rel_x2 = 0.42, 0.58
    rel_y1, rel_y2 = 0.155, 0.195
    
    res = detect_text_in_region(window, (rel_x1, rel_y1, rel_x2, rel_y2))
    print(res)
    if res == "Starting Hand" or res == "STANTINGINAND" or res == "STARTINGHAND" or res == "STARTINGIHAND" or res == "STANTINGINAND|" or "STANTING" in res or "STARTING" in res:
        return True

    if res is None:
        return None
    
    return False