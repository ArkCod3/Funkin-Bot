'''Real time Python bot to auto play Friday Night Funkin'.'''
import numpy as np
from mss import mss
import cv2
import pyautogui
import pydirectinput
import keyboard
import json
import os

#STEP ONE: Run program and open a song in the game. 
#STEP TWO: Click on the terminal and hover over the center of the specified arrow.
#STEP THREE: Hit enter when mouse is positioned. Repeat steps 2 and 3 for remaining arrows.
#If hits are late, then run program again and choose a lower point of the arrow.

pyautogui.PAUSE = 0
pydirectinput.PAUSE = 0

class Arrow():
    '''Class to track data for each arrow and react accordingly.
    Takes a position tuple (x,y), a BGR 8-bit color for the
    incoming arrows, a key character to press, and the arrow held
    color after a succesful hit.'''

    GRAY_COLOR = [173, 163, 135]
    WHITE_COLOR = [255, 255, 255]

    def __init__(self, position, color, key, hold_color):
        self.rel_pos = position
        self.color = color
        self.key = key
        self.was_hit = True
        self.hold_color = hold_color

    def update_arrow_state(self, img):
        read_color = list(img[self.rel_pos[1]][self.rel_pos[0]][:3])
        high_color = list(img[self.rel_pos[1]-offset_y][self.rel_pos[0]][:3])
        #higher position allows recognition of consecutive, fast notes

        if read_color != self.color or high_color == Arrow.WHITE_COLOR or high_color == self.hold_color:
            self.was_hit = True
            #was_hit prevents multiple presses for the same note

        elif self.was_hit:
            self.was_hit = False
            pydirectinput.keyUp(self.key)
            pydirectinput.keyDown(self.key)
            print(f'Pressed "{self.key}" key')

        return None

    def update_position(self, new_pos):
        self.rel_pos = new_pos
        return None

    def get_abs_pos(self):
        print(f'Place cursor on the arrow for key "{self.key}".')
        print('Press "shift" to confirm position.')
        keyboard.wait("shift")
        self.abs_pos = pyautogui.position()
        return None

def make_monitor(abs_positions):
    '''Intakes a list of game arrow absolute positions in 
    (x,y) format. Outputs the corresponding mss() monitor 
    for image capture, and the relative positions of all 
    arrows within that monitor.'''

    #Use absolute arrow positions to construct playing area
    raw_width = abs_positions[-1][0]-abs_positions[0][0]
    box_width = int(raw_width*1.3)
    box_height = int(box_width*0.24)
    box_left = int(abs_positions[0][0]-raw_width*0.15)
    box_top = int(abs_positions[0][1]-box_height*11/16)

    monitor_box = {'top':box_top, 'left': box_left,
    'width': box_width, 'height':box_height}

    #Redefine relative arrow positions within playing area
    rel_pos0 = (int(raw_width*0.15), int(box_height*11/16))

    rel_positions = [rel_pos0]
    for abs_pos in abs_positions[1:]:
        vector_x = abs_pos[0] - abs_positions[0][0]
        vector_y = abs_pos[1] - abs_positions[0][1]
        rel_positions.append((rel_pos0[0]+vector_x,rel_pos0[1]+vector_y))

    return monitor_box, rel_positions

if __name__ == '__main__':
    filename = input('Enter configuration name: ')
    path = os.path.join('configs',filename+'.json')
    with open(path) as f:
        settings = json.load(f)

    LEFT_COLOR = settings['left_color']
    DOWN_COLOR = settings['down_color']
    UP_COLOR = settings['up_color']
    RIGHT_COLOR = settings['right_color']

    LEFT_HOLD = settings['left_hold']
    DOWN_HOLD = settings['down_hold']
    UP_HOLD = settings['up_hold']
    RIGHT_HOLD = settings['right_hold']

    left_arrow = Arrow((0,0),LEFT_COLOR,'a',LEFT_HOLD)
    down_arrow = Arrow((0,0),DOWN_COLOR,'s',DOWN_HOLD)
    up_arrow = Arrow((0,0),UP_COLOR,'w', UP_HOLD)
    right_arrow = Arrow((0,0),RIGHT_COLOR,'d', RIGHT_HOLD)

    arrows = [left_arrow, down_arrow, up_arrow, right_arrow]

    absolute_positions = []
    for arrow in arrows:
        arrow.get_abs_pos()
        absolute_positions.append(arrow.abs_pos)
    pyautogui.alert('Arrow positions defined. \
    click "OK" to start bot.')

    arrow_box, rel_positions = make_monitor(absolute_positions)
    offset_y = int(arrow_box['height']*0.4)

    for arrow, rel_position in zip(arrows,rel_positions):
        arrow.update_position(rel_position)

    while True:
        with mss() as sct:
            img = np.array(sct.grab(arrow_box))

        for arrow in arrows:
            arrow.update_arrow_state(img)

        for position in rel_positions:
            cv2.circle(img, position, 4, [255,0,0], -1)
            cv2.circle(img, (position[0],position[1]-offset_y), 4, [255,0,0], -1)

        cv2.imshow('Arrow_Box',img)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break

    cv2.destroyAllWindows