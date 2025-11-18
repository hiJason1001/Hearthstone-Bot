
import pyautogui
import pygetwindow as gw
import time
import exit_bot
from read_turn_state import read_turn_state
from read_start_game import in_starting_hand
from read_replace_hand_wait import read_replace_hand_wait
from coords import *
from game_bot import GameBot

keyboard_listener = exit_bot.start_listener()

bot = GameBot()
    
while not exit_bot.exit:
    if not bot.update_window():
        print("NOT IN HEARTHSTONE")
        time.sleep(2)
        continue
    
    window = gw.getWindowsWithTitle("Hearthstone")[0]

    turn = read_turn_state(window)
    if (turn is None):
        print("PLAYER NOT IN GAME OR ERROR")
        time.sleep(1)
        continue
    if (turn == "UNKNOWN"):
        print("IDK WHO'S TURN IT IS")
        time.sleep(1)
        continue
    if bot.replace_hand:
        while not in_starting_hand(window):
            time.sleep(0.5)

        bot.confirm_replace_hand()
        time.sleep(5)
        while read_replace_hand_wait(window):
            time.sleep(0.5)
        time.sleep(5)
        bot.reset()
        continue
        
    if turn == "ENEMY_TURN":
        print("Waiting for enemy's turn")
        bot.reset()
        time.sleep(1)
        continue
    
    # must be player turn
    cards_to_play = cards_x
    if bot.turn_count == 1:
        cards_to_play = [cards_x[1], cards_x[3], cards_x[7], cards_x[9]]
    elif bot.turn_count == 2:
        cards_to_play = [cards_x[0], cards_x[2], cards_x[4], cards_x[6], cards_x[8], cards_x[9]]
        
    for x in cards_to_play:
        bot.play_one_card(x)
        if exit_bot.exit:
            break
        
    if exit_bot.exit:
        break
    
    bot.play_hero_power()
    if exit_bot.exit:
        break

    bot.play_weapon()
    if exit_bot.exit:
        break
    
    for minnion_x in player_minnions_x:
        bot.play_one_minnion(minnion_x)
        if exit_bot.exit:
            break        

    bot.end_turn()

    time.sleep(1)

keyboard_listener.stop()

