import cv2
import numpy as np
import pyautogui
import pytesseract
from coords import *

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def detect_text_in_region(window, rel_coords):
    if (
        window is None or
        window.width <= 0 or window.height <= 0 or
        window.isMinimized or
        window.left < 0 or window.top < 0
    ):
        print("ERROR: Bad WINDOW passed to detect_text_in_region")
        return None

    screenshot = pyautogui.screenshot(region=(
        window.left,
        window.top,
        window.width,
        window.height
    ))
    # screenshot = cv2.imread("imgs/starting_hand.png")
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    height, width, _ = screenshot.shape

    rel_x1, rel_y1, rel_x2, rel_y2 = rel_coords
    x1, y1 = int(rel_x1 * width), int(rel_y1 * height)
    x2, y2 = int(rel_x2 * width), int(rel_y2 * height)

    # DEBUG
    # debug_img = screenshot.copy()
    # cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow("Debug ROI", debug_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    roi = screenshot[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    processed = cv2.dilate(thresh, np.ones((1, 1), np.uint8), iterations=1)

    raw = pytesseract.image_to_string(processed, config='-l eng --psm 6')
    text = raw.strip().upper().replace("\n", " ")
    
    return text


def read_replace_hand_wait(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in read_replace_hand_wait")
        return None

    res = detect_text_in_region(window, (oppponent_still_choose_x1, oppponent_still_choose_y1, oppponent_still_choose_x2, oppponent_still_choose_y2))
    
    if "OPPONEN" in res or res == "OPPONENTS TLLICHOOSINGS" or res == "OPPONENT STILL CHOOSING..." or res == "OPPONENTS TILLICHOOSINGS" or res == "(OPPONENTS TLLICHOOSINGS":
        return True
    
    return False

def in_starting_hand(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in in_starting_hand")
        return None
    
    res = detect_text_in_region(window, (start_game_x1, start_game_y1, start_game_x2, start_game_y2))
    print(res)
    if res == "Starting Hand" or res == "STANTINGINAND" or res == "STARTINGHAND" or res == "STARTINGIHAND" or res == "STANTINGINAND|" or "STANTING" in res or "STARTING" in res:
        return True

    if res is None:
        return None
    
    return False

def read_turn_state(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in read_turn_state")
        return None

    res = detect_text_in_region(window, (turn_box_x1, turn_box_y1, turn_box_x2, turn_box_y2))

    if res == "END TURN" or res == "YOUR TURN":
        return "PLAYER_TURN"
    elif res == "ENEMY TURN" or res == "NEMY TURN" or "NEMY TURN" in res:
        return "ENEMY_TURN"
    
    return "UNKNOWN"

def in_play_menu(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in in_play_menu")
        return None

    res = detect_text_in_region(window, (menu_play_x1, menu_play_y1, menu_play_x2, menu_play_y2))
    print(res)
    if "LAY" in res or "PLA" in res or "PLAY" in res or "A.) MA" in res:
        return True

    return False

def in_queue(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in in_queue")
        return None

    res = detect_text_in_region(window, (queue_finding_opponent_x1, queue_finding_opponent_y1, queue_finding_opponent_x2, queue_finding_opponent_y2))

    if "FINDING" in res or "OPPONENT" in res or "INDIN" in res or "PPONEN" in res:
        return True

    return False

def error_in_queue(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in error_in_queue")
        return None

    res = detect_text_in_region(window, (error_finding_match_x1, error_finding_match_y1, error_finding_match_x2, error_finding_match_y2))

    if "ERROR" in res or "ERRO" in res or "RROR" in res:
        return True

    return False

def found_match(window, PVP=True):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in found_match")
        return None
    
    if USERNAME is None or USERNAME == "":
        print("ERROR in found_match: Bad username set in coords.py")
        return None

    if PVP:
        res = detect_text_in_region(window, (found_match_x1, found_match_y1, found_match_x2, found_match_y2))
    else:
        res = detect_text_in_region(window, (found_match_PVE_x1, found_match_PVE_y1, found_match_PVE_x2, found_match_PVE_y2))
    
    if USERNAME in res or USERNAME[1:] in res or USERNAME[:-1] in res:
        return True

    return False

def game_over(window):
    if window is None or window.width <= 0 or window.height <= 0 or window.isMinimized or window.left < 0 or window.top < 0:
        print("ERROR: Bad WINDOW in game_over")
        return None

    res = detect_text_in_region(window, (click_to_continue_x1, click_to_continue_y1, click_to_continue_x2, click_to_continue_y2))
    print(res)
    if "CLICK TO CONTINUE" in res or "CLICK" in res or "CONTINU" in res or "CLICH" in res or "CLICHÉ" in res or "ANTIN" in res or "TIANTI" in res:
        return True

    return False

"""
DOESNT WORK
"""
def detect_digits_in_region(window, rel_coords):
    if (
        window is None or
        window.width <= 0 or window.height <= 0 or
        window.isMinimized or
        window.left < 0 or window.top < 0
    ):
        print("ERROR: Bad WINDOW passed to detect_digits_in_region")
        return None

    screenshot = pyautogui.screenshot(region=(
        window.left,
        window.top,
        window.width,
        window.height
    ))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    

    height, width, _ = screenshot.shape
    rel_x1, rel_y1, rel_x2, rel_y2 = rel_coords
    x1, y1 = int(rel_x1 * width), int(rel_y1 * height)
    x2, y2 = int(rel_x2 * width), int(rel_y2 * height)
    # debug_img = screenshot.copy()
    # cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow("Debug ROI", debug_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    roi = screenshot[y1:y2, x1:x2]
    
    DIGIT_TEMPLATES = {}
    for d in range(10):
        img = cv2.imread(f"template_imgs/{d}.png", cv2.IMREAD_GRAYSCALE)
        DIGIT_TEMPLATES[d] = img
    def match_single_digit(roi_gray):
        best_digit = None
        best_score = -1

        for digit, tmpl in DIGIT_TEMPLATES.items():
            resized = cv2.resize(roi_gray, (tmpl.shape[1], tmpl.shape[0]))

            result = cv2.matchTemplate(resized, tmpl, cv2.TM_CCOEFF_NORMED)

            score = result[0][0]
            if score > best_score:
                best_score = score
                best_digit = digit

        return best_digit, best_score


    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    digit, score = match_single_digit(gray)
    return digit