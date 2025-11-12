import pygetwindow as gw
import pyautogui
import time
import exit_bot

# Start keyboard listener
listener = exit_bot.start_listener()

while not exit_bot.exit:
    active_window = gw.getActiveWindow()
    if not active_window or active_window.title != "Hearthstone":
        time.sleep(0.5)
        continue
    
    
    # print("Hearthstone is the active window")
    # window = gw.getWindowsWithTitle("Hearthstone")[0]

    # # Get coordinates and size
    # x, y = window.left, window.top
    # width, height = window.width, window.height

    # screenshot = pyautogui.screenshot(region=(x, y, width, height))
    # screenshot.save("hearthstone_window.png")
    
    # relative positions (0.0 - 1.0)
    hand_top_pct = 0.75      # top of the hand ~75% down the window
    hand_left_pct = 0.05     # left bound ~5% from window left
    hand_width_pct = 0.9     # hand width ~90% of window width
    hand_height_pct = 0.2    # hand height ~20% of window height

    hand_top = int(active_window.top + active_window.height * hand_top_pct)
    hand_left = int(active_window.left + active_window.width * hand_left_pct)
    hand_width = int(active_window.width * hand_width_pct)
    hand_height = int(active_window.height * hand_height_pct)

    hand_region = (hand_left, hand_top, hand_width, hand_height)
    hand_screenshot = pyautogui.screenshot(region=hand_region)
    hand_screenshot.save("hand.png")

    time.sleep(1)

listener.stop()
