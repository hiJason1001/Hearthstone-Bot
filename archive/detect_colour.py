import sys
import cv2
import numpy as np


image = cv2.imread("archive/imgs/starting_hand.png")
if image is None:
    print("Error: Image not found.")
    sys.exit(1)

height, width, _ = image.shape
rel_x1, rel_x2 = 0.78, 0.84
rel_y1, rel_y2 = 0.455, 0.485
x1 = int(rel_x1 * width)
y1 = int(rel_y1 * height)
x2 = int(rel_x2 * width)
y2 = int(rel_y2 * height)
roi = image[y1:y2, x1:x2]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])

mask = cv2.inRange(hsv_roi, lower_green, upper_green)

green_pixel_count = np.count_nonzero(mask)
total_pixels = mask.size
green_percentage = (green_pixel_count / total_pixels) * 100


print(f"Green pixel percentage in ROI: {green_percentage:.2f}%")

min_green_percentage = 30
if green_percentage >= min_green_percentage:
    print("The End Turn button is green (turn is likely over).")
else:
    print(
        "The End Turn button is not predominantly green (actions might be pending or an error occurred)."
    )
