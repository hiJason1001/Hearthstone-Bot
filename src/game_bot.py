import pygetwindow as gw
import pyautogui
from coords import *
from read_text import *
import exit_bot
import time

class GameBot:
    def __init__(self):
        self.window = None
        self.replace_hand = True
        self.turn_count = 1
        
    def update_window(self):
        windows = gw.getWindowsWithTitle("Hearthstone")
        if not windows:
            return False

        active = gw.getActiveWindow()
        if not active or active.title != "Hearthstone":
            return False

        self.window = active
        return True

        
    def convert_x(self, x):
        return self.window.left + x * self.window.width

    def convert_y(self, y):
        return self.window.top + y * self.window.height
    
    def reset(self):
        pyautogui.moveTo(self.convert_x(reset_x), self.convert_y(reset_y), duration=MOUSE_SPEED_FAST)
        pyautogui.rightClick()
        
    def confirm_replace_hand(self):
        pyautogui.moveTo(self.convert_x(confirm_replace_hand_x), self.convert_y(confirm_replace_hand_y), duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        self.replace_hand = False
        
    def play_one_card(self, x):        
        y = cards_y
        pyautogui.moveTo(self.convert_x(x), self.convert_y(y), duration=MOUSE_SPEED_FAST)
        pyautogui.mouseDown()
        pyautogui.moveTo(self.convert_x(enemy_face_x), self.convert_y(enemy_face_y), duration=MOUSE_SPEED_FAST)
        pyautogui.mouseUp()

        for minnion_x in enemy_minnions_x:
            pyautogui.moveTo(self.convert_x(minnion_x), self.convert_y(enemy_minnions_y), duration=MOUSE_SPEED_FAST)
            pyautogui.click()
            
        for minnion_x in player_minnions_x:
            pyautogui.moveTo(self.convert_x(minnion_x), self.convert_y(player_minnions_y), duration=MOUSE_SPEED_FAST)
            pyautogui.click()
        
        self.reset()
        
    def play_hero_power(self):
        pyautogui.moveTo(self.convert_x(player_hero_power_x), self.convert_y(player_hero_power_y), duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        
        pyautogui.moveTo(self.convert_x(enemy_face_x), self.convert_y(enemy_face_y), duration=MOUSE_SPEED_FAST)   
        pyautogui.click()
        
        # imbrue?????????
        for discover_x in discover3_x:
            pyautogui.moveTo(self.convert_x(discover_x), self.convert_y(discover3_y), duration=MOUSE_SPEED_FAST)
            pyautogui.click()
        
        self.reset()
        
    def play_weapon(self):
        pyautogui.moveTo(self.convert_x(player_face_x), self.convert_y(player_face_y), duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        pyautogui.moveTo(self.convert_x(enemy_face_x), self.convert_y(enemy_face_y), duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        for minnion_x in enemy_minnions_x:
            pyautogui.moveTo(self.convert_x(minnion_x), self.convert_y(enemy_minnions_y), duration=MOUSE_SPEED_FAST)
            pyautogui.click()
            
        self.reset()
        
    def play_one_minnion(self, minnion_x):
        pyautogui.moveTo(self.convert_x(minnion_x), self.convert_y(player_minnions_y), duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        
        pyautogui.moveTo(self.convert_x(enemy_face_x), self.convert_y(enemy_face_y), duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        for x in enemy_minnions_x:
            pyautogui.moveTo(self.convert_x(x), self.convert_y(enemy_minnions_y), duration=MOUSE_SPEED_FAST)
            pyautogui.click()
        
        self.reset()
        
    def end_turn(self):
        pyautogui.moveTo(self.convert_x(end_turn_button_x), self.convert_y(end_turn_button_y), duration=MOUSE_SPEED_FAST)
        pyautogui.click()
        self.reset()
        self.turn_count += 1
        
    def reset_bot(self):
        self.window = None
        self.replace_hand = True
        self.turn_count = 1
        
    def run(self, SKIP=False):
        while not exit_bot.exit:
            if not self.update_window():
                print("NOT IN HEARTHSTONE")
                time.sleep(2)
                continue
            
            self.window = gw.getWindowsWithTitle("Hearthstone")[0]
            
            if game_over(self.window):
                return

            turn = read_turn_state(self.window)
            if turn is None:
                print("PLAYER NOT IN GAME OR ERROR")
                time.sleep(1)
                continue
            if turn == "UNKNOWN":
                print("IDK WHO'S TURN IT IS")
                time.sleep(1)
                continue
            
            if self.replace_hand:
                while not in_starting_hand(self.window):
                    time.sleep(0.5)

                self.confirm_replace_hand()
                time.sleep(5)
                while read_replace_hand_wait(self.window):
                    time.sleep(0.5)
                time.sleep(5)
                self.reset()
                continue
                
            if turn == "ENEMY_TURN":
                print("Waiting for enemy's turn")
                self.reset()
                time.sleep(1)
                continue
            
            # must be player turn
            if SKIP:
                time.sleep(1)
                self.end_turn()
                time.sleep(1)
                continue
                
            cards_to_play = cards_x
            if self.turn_count == 1:
                cards_to_play = [cards_x[1], cards_x[3], cards_x[7], cards_x[9]]
            elif self.turn_count == 2:
                cards_to_play = [cards_x[0], cards_x[2], cards_x[4], cards_x[6], cards_x[8], cards_x[9]]
                
            for x in cards_to_play:
                self.play_one_card(x)
                if exit_bot.exit or game_over(self.window):
                    return                
            
            self.play_hero_power()
            if exit_bot.exit or game_over(self.window):
                return 

            self.play_weapon()
            if exit_bot.exit or game_over(self.window):
                return
            
            for minnion_x in player_minnions_x:
                self.play_one_minnion(minnion_x)
                if exit_bot.exit or game_over(self.window):
                    return       

            self.end_turn()

            time.sleep(1)