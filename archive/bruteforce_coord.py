import cv2
import numpy as np
import pytesseract

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

cards = [0.34, 0.37, 0.40, 0.425, 0.45, 0.48, 0.50, 0.53, 0.56, 0.60]
minnions = [0.30, 0.37, 0.44, 0.5, 0.56, 0.63, 0.70]

screenshot = cv2.imread("archive/imgs/rewind.png")
height, width, _ = screenshot.shape 
# for x in minnions:
#     x1 = int(x * width)
#     y1 = int(0.39 * height)

#     cv2.circle(screenshot, (x1, y1), 5, (0, 0, 255), -1)
#     cv2.imshow("Test Point", screenshot)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

x = 0.3
y = 0.75
x1 = int(x * width)
y1 = int(y * height)
cv2.circle(screenshot, (x1, y1), 5, (0, 0, 255), -1)
cv2.imshow("Test Point", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()

# rel_x1, rel_x2 = 0.41, 0.59
# rel_y1, rel_y2 = 0.92, 0.96
# x1 = int(rel_x1 * width)
# y1 = int(rel_y1 * height)
# x2 = int(rel_x2 * width)
# y2 = int(rel_y2 * height) 
# cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
# cv2.imshow("Test Point", screenshot)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


roi = screenshot[y1:y2, x1:x2]
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = np.ones((2, 2), np.uint8)
processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
config = "-l eng --psm 7"
raw = pytesseract.image_to_string(processed, config=config)
text = raw.strip().upper()
print(text)