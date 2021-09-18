from funkin_bot import Arrow, make_monitor
import cv2; from mss import mss
import keyboard, pyautogui, pydirectinput
import numpy as np
from time import perf_counter
import os, json

pyautogui.PAUSE = 0
pydirectinput.PAUSE = 0

FILL_COL = [0,0,0]
class ArrowBuilder(Arrow):
    def color_defined(self, img):
        if self.color != self.idle_color:
            return True #color is already defined

        read_color = (img[self.rel_pos[1]][self.rel_pos[0]][:3]).tolist()
        high_color = (img[self.rel_pos[1]-offset_y][self.rel_pos[0]][:3]).tolist()
        #higher position allows recognition of consecutive, fast notes

        if high_color == self.idle_color:
            return False

        self.color = read_color
        self.prev_color = high_color
        self.timer = perf_counter()
        pydirectinput.keyUp(self.key)
        pydirectinput.keyDown(self.key)
        print(f'Arrow color defined for "{self.key}" key')
        return True

    def hold_defined(self,img):
        if self.hold_color != self.idle_color:
            return True #Hold color was already defined

        #read_color = list(img[self.rel_pos[1]][self.rel_pos[0]][:3])
        high_color = (img[self.rel_pos[1]-offset_y][self.rel_pos[0]][:3]).tolist()
        
        if high_color == self.color or high_color != self.prev_color: 
            self.timer = perf_counter()
            self.prev_color = high_color
            return False

        if perf_counter() < self.timer + 0.25:
            return False #wait until hold_color shows up

        self.hold_color = high_color
        return True
        
left_arrow = ArrowBuilder((0,0),FILL_COL,'a',FILL_COL)
down_arrow = ArrowBuilder((0,0),FILL_COL,'s',FILL_COL)
up_arrow = ArrowBuilder((0,0),FILL_COL,'w', FILL_COL)
right_arrow = ArrowBuilder((0,0),FILL_COL,'d', FILL_COL)

arrows = [left_arrow, down_arrow, up_arrow, right_arrow]

absolute_positions = []
for arrow in arrows:
    arrow.get_abs_pos()
    absolute_positions.append(arrow.abs_pos)
print('Arrow positions defined.')

arrow_box, rel_positions = make_monitor(absolute_positions)
offset_y = int(arrow_box['height']*0.4)

print('Unpause your game and press "shift".')
keyboard.wait('shift')

with mss() as sct:  #Capture to define idle colors
        img = np.array(sct.grab(arrow_box))

for arrow, rel_position in zip(arrows,rel_positions):
    arrow.update_position(rel_position)
    arrow.idle_color = list(img[rel_position[1]][rel_position[0]][:3])
    arrow.color = arrow.idle_color
    arrow.hold_color = arrow.idle_color

#Find the arrow's color, and then play until hold color 
#can be extracted.

while True:
    with mss() as sct:
        img = np.array(sct.grab(arrow_box))

    arrow_defined_count = 0
    for arrow in arrows:
        if not arrow.color_defined(img):
            continue
        if arrow.hold_defined(img):
            arrow_defined_count += 1

    if arrow_defined_count == 4:
        print('Color data gathered.')
        break

    for position in rel_positions:
        cv2.circle(img, position, 4, [255,0,0], -1)
        cv2.circle(img, (position[0],position[1]-offset_y), 4, [255,0,0], -1)

    cv2.imshow('Arrow_Box',img)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cv2.destroyAllWindows
pyautogui.alert('Color data collected.')

setting_vals = []
for arrow in arrows:
    setting_vals.append(arrow.color)
    setting_vals.append(arrow.hold_color)

settings = ['left_color','left_hold','down_color','down_hold',
'up_color','up_hold','right_color','right_hold']

data = {}
for setting, val in zip(settings,setting_vals):
    data[setting] = val

print(data)
filename = input('Enter configuration name: ')
file_path = os.path.join('configs',filename+'.json')
with open(file_path, 'w') as f:
    json.dump(data, f, indent=1)