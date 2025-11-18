import pygetwindow as gw
import pyautogui
from coords import *

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
        
        pyautogui.moveTo(self.convert_x(enemy_face_x), self.convert_y(enemy_face_y), duration=MOUSE_SPEED) # enemy face
        pyautogui.click()
        for x in enemy_minnions_x:
            pyautogui.moveTo(self.convert_x(x), self.convert_y(enemy_minnions_y), duration=MOUSE_SPEED_FAST)
            pyautogui.click()
        
        self.reset()
        
    def end_turn(self):
        pyautogui.moveTo(self.convert_x(end_turn_button_x), self.convert_y(end_turn_button_y), duration=MOUSE_SPEED)
        pyautogui.click()
        self.reset()
        self.turn_count += 1