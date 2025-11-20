import pygetwindow as gw
import time
import exit_bot
from read_text import *
from game_bot import GameBot

"""
CONFIG
"""
PVP = True
SKIP_TURNS = False

keyboard_listener = exit_bot.start_listener()

bot = GameBot()

while not exit_bot.exit:
    time.sleep(0.5)
    
    windows = gw.getWindowsWithTitle("Hearthstone")
    active = gw.getActiveWindow()
    if not windows or not active or active.title != "Hearthstone":
        print("NOT IN HEARTHSTONE")
        time.sleep(1)
        continue
    
    window = gw.getWindowsWithTitle("Hearthstone")[0]
    
    """
    if in play menu, press play and continue
    if in queue wait
    if game ended, wait until back in play menu
    """
    
    if error_in_queue(window):
        print("encountered error in queue but player exited queue")
        time.sleep(4)
        pyautogui.moveTo(window.left + error_finding_match_ok_x * window.width, window.top + error_finding_match_ok_y * window.height, duration=MOUSE_SPEED)
        pyautogui.click()
        if exit_bot.exit:
            break
        time.sleep(4)
    
    if in_play_menu(window):
        time.sleep(4)
        if exit_bot.exit:
            break
        pyautogui.moveTo(window.left + menu_play_x * window.width, window.top + menu_play_y * window.height, duration=MOUSE_SPEED)
        pyautogui.click()
        continue
    
    while in_queue(window):
        print("in queue")
        if error_in_queue(window):
            print("encountered error in queue")
            time.sleep(4)
            pyautogui.moveTo(window.left + error_finding_match_ok_x * window.width, window.top + error_finding_match_ok_y * window.height, duration=MOUSE_SPEED)
            pyautogui.click()
            if exit_bot.exit:
                break
            time.sleep(4)
            break
        time.sleep(6)
    
    if found_match(window, PVP):
        bot.run(SKIP_TURNS)
        if exit_bot.exit:
            break
        
        while game_over(window):
            pyautogui.moveTo(window.left + reset_x * window.width, window.top + reset_y * window.height, duration=MOUSE_SPEED)
            pyautogui.click()
            time.sleep(0.5)
            if exit_bot.exit:
                break
        
        bot.reset_bot()
        time.sleep(4)
        continue
    
    print("How did I get here?")
    

keyboard_listener.stop()

