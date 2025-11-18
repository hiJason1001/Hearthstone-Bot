from read_text import detect_text_in_region

def read_turn_state(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in get_turn_state")
        return None

    rel_x1, rel_x2 = 0.78, 0.84
    rel_y1, rel_y2 = 0.455, 0.485

    res = detect_text_in_region(window, (rel_x1, rel_y1, rel_x2, rel_y2))

    if res == "END TURN" or res == "YOUR TURN":
        return "PLAYER_TURN"
    elif res == "ENEMY TURN" or res == "NEMY TURN" or "NEMY TURN" in res:
        return "ENEMY_TURN"
    
    return "UNKNOWN"