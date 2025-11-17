import cv2
import numpy as np
import pyautogui
import pytesseract

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