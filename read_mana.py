"""
DOESNT WORK
"""

from read_text import detect_text_in_region, detect_digits_in_region

def read_mana(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in get_mana")
        return None

    rel_x1 = 0.635
    rel_y1 = 0.911
    rel_x2 = 0.644
    rel_y2 = 0.933
    
    digit1 = detect_digits_in_region(window, (rel_x1, rel_y1, rel_x2, rel_y2))
    
    rel_x1 = 0.647
    rel_y1 = 0.911
    rel_x2 = 0.655
    rel_y2 = 0.932
    digit2 = detect_digits_in_region(window, (rel_x1, rel_y1, rel_x2, rel_y2))
    return digit1, digit2