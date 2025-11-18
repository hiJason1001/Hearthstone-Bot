import pygetwindow as gw
import pyautogui
import time
import exit_bot
import cv2


img = cv2.imread("imgs/hand.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)
# cv2.imwrite("imgs/gray_debug.png", gray)
# cv2.imwrite("imgs/blur_debug.png", blur)
cv2.imwrite("imgs/edges_debug.png", edges)


# contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# card_contours = []
# for c in contours:
#     x, y, w, h = cv2.boundingRect(c)
#     aspect_ratio = w / float(h)
#     if 0.6 < aspect_ratio < 0.8 and w > 30 and h > 50:
#         card_contours.append((x, y, w, h))

# print(len(card_contours))