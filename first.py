import pyautogui
import pygetwindow as gw
import time
import exit_bot
from read_turn_state import read_turn_state
from read_mana import read_mana
from read_start_game import in_starting_hand
from read_replace_hand_wait import read_replace_hand_wait

replace_hand = True
keyboard_listener = exit_bot.start_listener()
turn_count = 0

MOUSE_SPEED = 0.2
MOUSE_SPEED_FAST = 0.005

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

enemy_minnions_x = [0.315, 0.385, 0.45, 0.5, 0.55, 0.615, 0.685]
enemy_minnions_y = 0.39
player_minnions_x = [0.315, 0.385, 0.45, 0.5, 0.55, 0.615, 0.685]
player_minnions_y = 0.555
    
def reset():
    pyautogui.moveTo(window.left + 0.9 * width, window.top + 0.8 * height, duration=MOUSE_SPEED_FAST)
    pyautogui.rightClick()
    
while not exit_bot.exit:
    active_window = gw.getActiveWindow()
    if not active_window or active_window.title != "Hearthstone":
        print("NOT IN HEARTHSTONE")
        time.sleep(3)
        continue
    
    window = gw.getWindowsWithTitle("Hearthstone")[0]
    width = window.width
    height = window.height

    # x, y = window.left, window.top
    # screenshot = pyautogui.screenshot(region=(x, y, width, height))
    # screenshot.save("hearthstone_window.png")
    # break

    turn = read_turn_state(window)
    if (turn is None):
        print("PLAYER NOT IN GAME OR ERROR")
        time.sleep(1)
        continue
    if (turn == "UNKNOWN"):
        print("IDK WHO'S TURN IT IS")
        time.sleep(1)
        continue
    if replace_hand:
        while not in_starting_hand(window):
            time.sleep(0.5)

        pyautogui.moveTo(window.left + 0.5 * width, window.top + 0.79 * height, duration=MOUSE_SPEED)
        pyautogui.click()
        replace_hand = False
        time.sleep(5)
        while read_replace_hand_wait(window):
            time.sleep(0.5)
        time.sleep(5)
        reset()
        continue
        
    if turn == "ENEMY_TURN":
        print("Waiting for enemy's turn")
        reset()
        time.sleep(1)
        continue
    
    # must be player turn
    turn_count += 1
    target_x = int(0.5 * width)
    target_y = int(0.2 * height)
    cards_to_play = cards
    if turn_count == 1:
        cards_to_play = [cards[0], cards[2], cards[5], cards[7]]
    elif turn_count == 2:
        cards_to_play = [cards[0], cards[2], cards[4], cards[6], cards[8], cards[9]]
    elif turn_count == 3:
        cards_to_play = cards[1:9]
        
    for (rel_x1, rel_x2) in cards_to_play:
        rel_y1 = 0.9
        rel_y2 = 1
        x1 = int(rel_x1 * width)
        y1 = int(rel_y1 * height)
        x2 = int(rel_x2 * width)
        y2 = int(rel_y2 * height)
        start_x = int((x1 + x2) / 2 + (x2 - x1) * 0.2)
        start_y = int((y1 + y2) / 2)
        
        # drag curr card to enemy face
        pyautogui.moveTo(window.left + start_x, window.top + start_y, duration=MOUSE_SPEED)
        pyautogui.mouseDown()
        pyautogui.moveTo(window.left + target_x, window.top + target_y, duration=MOUSE_SPEED) # enemy face
        pyautogui.mouseUp()

        for minnion_x in enemy_minnions_x:
            pyautogui.moveTo(window.left + minnion_x * width, window.top + enemy_minnions_y * height, duration=MOUSE_SPEED_FAST)
            pyautogui.click()
            
        for minnion_x in player_minnions_x:
            pyautogui.moveTo(window.left + minnion_x * width, window.top + player_minnions_y * height, duration=MOUSE_SPEED_FAST)
            pyautogui.click()
        
        reset()
        if exit_bot.exit:
            break
        
    if exit_bot.exit:
        break
    # hero power, click, then move, then click again
    pyautogui.moveTo(window.left + int(0.6 * width), window.top + int(0.75 * height), duration=MOUSE_SPEED)
    pyautogui.click()
    # enemy face
    pyautogui.moveTo(window.left + target_x, window.top + target_y, duration=MOUSE_SPEED)
    pyautogui.click()
    # discover 3 (imbrue?????????)
    pyautogui.moveTo(window.left + int(0.31 * width), window.top + int(0.5 * height), duration=MOUSE_SPEED_FAST)
    pyautogui.click()
    pyautogui.moveTo(window.left + int(0.5 * width), window.top + int(0.5 * height), duration=MOUSE_SPEED_FAST)
    pyautogui.click()
    pyautogui.moveTo(window.left + int(0.69 * width), window.top + int(0.5 * height), duration=MOUSE_SPEED_FAST)
    pyautogui.click()
    
    reset()
    if exit_bot.exit:
        break

    # weapon
    pyautogui.moveTo(window.left + int(0.5 * width), window.top + int(0.75 * height), duration=MOUSE_SPEED_FAST) # player face
    pyautogui.click()
    pyautogui.moveTo(window.left + target_x, window.top + target_y, duration=MOUSE_SPEED) # enemy face
    pyautogui.click()
    for minnion_x in enemy_minnions_x:
        pyautogui.moveTo(window.left + minnion_x * width, window.top + enemy_minnions_y * height, duration=MOUSE_SPEED_FAST)
        pyautogui.click()
    reset()
    if exit_bot.exit:
        break
    
    # perform minnion actions
    for minnion_x in player_minnions_x:
        pyautogui.moveTo(window.left + minnion_x * width, window.top + player_minnions_y * height, duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        
        pyautogui.moveTo(window.left + target_x, window.top + target_y, duration=MOUSE_SPEED) # enemy face
        pyautogui.click()
        for minnion_x in enemy_minnions_x:
            pyautogui.moveTo(window.left + minnion_x * width, window.top + enemy_minnions_y * height, duration=MOUSE_SPEED_FAST)
            pyautogui.click()
        reset()
        if exit_bot.exit:
            break
        
        

    # end turn
    pyautogui.moveTo(window.left + 0.8 * width, window.top + 0.46 * height, duration=MOUSE_SPEED)
    pyautogui.click()

    time.sleep(1)

keyboard_listener.stop()




"""
hand_top_pct = 0.8      # Ignores 80% of window from the top
hand_left_pct = 0.2     # Ignores 20% of window from left and right

hand_top = int(active_window.top + active_window.height * hand_top_pct)
hand_left = int(active_window.left + active_window.width * hand_left_pct)
hand_width = int(active_window.width * (1 - 2 * hand_left_pct))
hand_height = int(active_window.height * (1 - hand_top_pct))

hand_screenshot = pyautogui.screenshot(region=(hand_left, hand_top, hand_width, hand_height))
hand_screenshot.save("hand.png")
"""