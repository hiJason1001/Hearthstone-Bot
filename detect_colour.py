import cv2
import numpy as np

# --- Define HSV Color Ranges ---
# These are moved outside the function for clarity and global use.
LOWER_GREEN = np.array([40, 50, 50])
UPPER_GREEN = np.array([80, 255, 255])
LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([40, 255, 255])
# Package the ranges into a dictionary for easy iteration
COLOR_RANGES = {
    "green": {"lower": LOWER_GREEN, "upper": UPPER_GREEN},
    "yellow": {"lower": LOWER_YELLOW, "upper": UPPER_YELLOW},
}

def detect_card_border(screenshot, card_coords, color_ranges, min_color_percentage=0.05):
    """
    Checks if a card within the given coordinates has a green or yellow border.

    Args:
        screenshot (np.array): The full screenshot image (BGR).
        card_coords (tuple): (x_min, y_min, x_max, y_max) defining the card area.
        color_ranges (dict): Dictionary mapping color names to their lower/upper HSV bounds.
        min_color_percentage (float): Minimum percentage of color pixels required 
                                      in the border ROI to be considered.

    Returns:
        str or None: The name of the detected border color ("green", "yellow"), 
                     or None if no significant border is found.
    """
    x1, y1, x2, y2 = card_coords
    
    # 1. Define the Border Region of Interest (ROI)
    border_thickness = 10
    
    # Define a slightly larger area to sample the border
    border_x1 = max(0, x1 - border_thickness)
    border_y1 = max(0, y1 - border_thickness)
    border_x2 = min(screenshot.shape[1], x2 + border_thickness)
    border_y2 = min(screenshot.shape[0], y2 + border_thickness)
    
    # Crop the border ROI
    border_roi = screenshot[border_y1:border_y2, border_x1:border_x2]

    # Check for empty ROI
    if border_roi.size == 0:
        return None

    # 2. Convert ROI to HSV
    hsv_roi = cv2.cvtColor(border_roi, cv2.COLOR_BGR2HSV)
    total_roi_pixels = border_roi.shape[0] * border_roi.shape[1]
    
    if total_roi_pixels == 0:
        return None
        
    # 3. Iterate and check for all colors
    for color_name, hsv_bounds in color_ranges.items():
        lower = hsv_bounds["lower"]
        upper = hsv_bounds["upper"]

        # Create a mask for the current color
        color_mask = cv2.inRange(hsv_roi, lower, upper)
        
        # Calculate the percentage of this color pixels
        total_color_pixels = cv2.countNonZero(color_mask)
        color_percentage = total_color_pixels / total_roi_pixels

        # 4. Determine if the color is present
        if color_percentage >= min_color_percentage:
            return color_name # Found the color, return it immediately

    return None # No significant color border found


screenshot = cv2.imread("imgs/yellow.png")

if screenshot is None:
    print("Error: Could not load screenshot image.")
else:
    height, width, _ = screenshot.shape 
    
    rel_x1, rel_x2 = 0.46, 0.48
    rel_y1, rel_y2 = 0.90, 1.00
    
    x1 = int(rel_x1 * width)
    y1 = int(rel_y1 * height)
    x2 = int(rel_x2 * width)
    y2 = int(rel_y2 * height)
    card_1_coords = (x1, y1, x2, y2) # (x_min, y_min, x_max, y_max)

    detected_color = detect_card_border(
        screenshot, 
        card_1_coords, 
        COLOR_RANGES,
        min_color_percentage=0.08 # Adjusted threshold slightly
    )

    print(f"{detected_color}")
    
    if detected_color == "green":
        draw_color = (0, 255, 0) # BGR green
    elif detected_color == "yellow":
        draw_color = (0, 255, 255) # BGR yellow
    else:
        draw_color = (255, 255, 255) # White for not detected

    cv2.rectangle(screenshot, (x1, y1), (x2, y2), draw_color, 3)
    cv2.imshow("Detected Card", screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()