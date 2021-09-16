'''Real time Python bot to auto play Friday Night Funkin'.'''
import numpy as np
from mss import mss
import cv2
import pyautogui

#STEP ONE: Run program and open a song in the game. 
#STEP TWO: Click on the terminal and hover over the center of the specified arrow.
#STEP THREE: Hit enter when mouse is positioned. Repeat steps 2 and 3 for remaining arrows.
#If hits are late, then run program again and choose a lower point of the arrow.

pyautogui.PAUSE = 0

LEFT_COLOR = [153, 75, 194]
DOWN_COLOR = [255, 255, 0]
UP_COLOR = [5, 250, 18]
RIGHT_COLOR = [63, 57, 249]
GRAY_COLOR = [173, 163, 135]
WHITE_COLOR = [255, 255, 255]

LEFT_HOLD = [255, 218, 255]
DOWN_HOLD = [255, 255, 142]
UP_HOLD = [177, 255, 148]
RIGHT_HOLD = [220, 204, 255]

class Arrow():
    '''Class to track data for each arrow and react accordingly.
    Takes a position tuple (x,y), a BGR 8-bit color for the
    incoming arrows, a key character to press, and the arrow held
    color after a succesful hit.'''

    def __init__(self, position, color, key, hold_color):
        self.position = position
        self.color = color
        self.key = key
        self.was_hit = True
        self.streak = 0
        self.hold_color = hold_color

    def update_arrow_state(self, img):
        read_color = list(img[self.position[1]][self.position[0]][:3])
        high_color = list(img[self.position[1]-offset_y][self.position[0]][:3])
        #higher position allows recognition of consecutive, fast notes

        if read_color != self.color or high_color == WHITE_COLOR or high_color == self.hold_color:
            self.was_hit = True
            #was_hit prevents multiple presses for the same note

        elif self.was_hit:
            self.was_hit = False
            pyautogui.keyUp(self.key)
            pyautogui.keyDown(self.key)
            print(f'Pressed "{self.key}" key')

        return None

    def update_position(self, new_pos):
        self.position = new_pos
        return None

    def get_abs_pos(self):
        print(f'Place mouse on the arrow for key "{self.key}".')
        input('Hit enter to confirm position.\n')
        return pyautogui.position()

left_arrow = Arrow((0,0),LEFT_COLOR,'A',LEFT_HOLD)
down_arrow = Arrow((0,0),DOWN_COLOR,'S',DOWN_HOLD)
up_arrow = Arrow((0,0),UP_COLOR,'W', UP_HOLD)
right_arrow = Arrow((0,0),RIGHT_COLOR,'D', RIGHT_HOLD)

arrows = [left_arrow, down_arrow, up_arrow, right_arrow]

abs_positions = []
for arrow in arrows:
    abs_positions.append(arrow.get_abs_pos())
print('Arrow positions defined.')

#Use absolute arrow positions to construct playing area
raw_width = abs_positions[-1][0]-abs_positions[0][0]
box_width = int(raw_width*1.3)
box_height = int(box_width*0.24)
box_left = int(abs_positions[0][0]-raw_width*0.15)
box_top = int(abs_positions[0][1]-box_height*11/16)
offset_y = int(box_height*0.4)

arrow_box = {'top':box_top, 'left': box_left,
'width': box_width, 'height':box_height}

#Redefine relative arrow positions within playing area
rel_pos0 = (int(raw_width*0.15), int(box_height*11/16))

rel_positions = [rel_pos0]
for abs_pos in abs_positions[1:]:
    vector_x = abs_pos[0] - abs_positions[0][0]
    vector_y = abs_pos[1] - abs_positions[0][1]
    rel_positions.append((rel_pos0[0]+vector_x,rel_pos0[1]+vector_y))

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