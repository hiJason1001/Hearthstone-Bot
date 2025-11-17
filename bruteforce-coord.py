import cv2
import numpy as np

cards = [0.34, 0.37, 0.40, 0.425, 0.45, 0.48, 0.50, 0.53, 0.56, 0.60]
minnions = [0.30, 0.37, 0.44, 0.5, 0.56, 0.63, 0.70]

screenshot = cv2.imread("imgs/starting_hand.png")
height, width, _ = screenshot.shape 
# for x in minnions:
#     x1 = int(x * width)
#     y1 = int(0.39 * height)

#     cv2.circle(screenshot, (x1, y1), 5, (0, 0, 255), -1)
#     cv2.imshow("Test Point", screenshot)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# x = 0.69
# y = 0.5
# x1 = int(x * width)
# y1 = int(y * height)
# cv2.circle(screenshot, (x1, y1), 5, (0, 0, 255), -1)
# cv2.imshow("Test Point", screenshot)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

rel_x1, rel_x2 = 0.42, 0.58
rel_y1, rel_y2 = 0.155, 0.195
x1 = int(rel_x1 * width)
y1 = int(rel_y1 * height)
x2 = int(rel_x2 * width)
y2 = int(rel_y2 * height) 
cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow("Test Point", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()




"""
OLD COORDS

Card Coord
y1 = 0.90
y2 = 1.00
     x1   x2   
cards = [
    (0.33, 0.35),
    (0.36, 0.38),
    (0.38, 0.41),
    (0.41, 0.43),
    (0.43, 0.46),
    (0.46, 0.48),
    (0.48, 0.50),
    (0.51, 0.525),
    (0.53, 0.55),
    (0.57, 0.60)
]

Hand card cursor coord:
let card coord be rel_x1, rel_y1, rel_x2, rel_y2, and img height and width
x1 = int(rel_x1 * width)
y1 = int(rel_y1 * height)
x2 = int(rel_x2 * width)
y2 = int(rel_y2 * height)
Coord is at (int((x2 + x1) / 2 + (x2 - x1) * 0.2), int((y2 + y1) / 2))


opponent face coord:
int(0.5 * width), int(0.2 * height)

player face coord:
int(0.5 * width), int(0.75 * height)

end turn button coord:
int(0.8 * width), int(0.46 * height)

hero power coord:
int(0.6 * width), int(0.75 * height)

opponent minnion coords:
x = 0.315, 0.385, 0.45, 0.5, 0.55, 0.615, 0.685
y = 0.39

player minnion coords:
x = 0.315, 0.385, 0.45, 0.5, 0.55, 0.615, 0.685
y = 0.555

confirm replace hand coord:
x = 0.5
y = 0.79

reset cursor coord:
x = int(0.9 * width)
y = int(0.8 * height)

discover 3 coords:
x = 0.31, 0.5, 0.69
y = 0.5



"""