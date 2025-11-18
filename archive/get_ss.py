import pyautogui
import pygetwindow as gw
import time
import exit_bot

keyboard_listener = exit_bot.start_listener()

while not exit_bot.exit:
    active_window = gw.getActiveWindow()
    if not active_window or active_window.title != "Hearthstone":
        print("NOT IN HEARTHSTONE")
        time.sleep(3)
        continue
    

window = gw.getWindowsWithTitle("Hearthstone")[0]
width = window.width
height = window.height
x, y = window.left, window.top
screenshot = pyautogui.screenshot(region=(x, y, width, height))
screenshot.save("hearthstone_window.png")
keyboard_listener.stop()



