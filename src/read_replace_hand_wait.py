from read_text import detect_text_in_region, detect_digits_in_region

def read_replace_hand_wait(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in read_replace_hand_wait")
        return None

    # Opponent still choosing rectangle
    rel_x1 = 0.418
    rel_y1 = 0.733
    rel_x2 = 0.585
    rel_y2 = 0.762
    
    res = detect_text_in_region(window, (rel_x1, rel_y1, rel_x2, rel_y2))
    
    print(res)
    if "OPPONEN" in res or res == "OPPONENTS TLLICHOOSINGS" or res == "OPPONENT STILL CHOOSING..." or res == "OPPONENTS TILLICHOOSINGS" or res == "(OPPONENTS TLLICHOOSINGS":
        return True
    
    return False

