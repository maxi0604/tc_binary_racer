#!/usr/bin/env python3
from pynput.mouse import Button, Controller
import numpy as np
import cv2
import pyscreenshot as ImageGrab
import pytesseract
from PIL import Image
import re
import time
import subprocess

display_size = (1920, 1080)
dx, dy = display_size
bbox = (800, 380, 1180, 580)
x1, y1, x2, y2 = bbox
bbox_ss = (x1 + dx, y1, x2 + dx, y2)
first_bit = (529, 949)
first_bit_s = (529 + dx, 949)
button_x_delta = 95
submit = (962, 1030)
submit_s = (962 + dx, 1030)
backwards_correction = -1
down = 40
upwards_correction = -1

def ydotool_run(args):
    print(" ".join(["ydotool"] + args))
    return subprocess.run(["ydotool"] + args, stdout=subprocess.PIPE).stdout.decode('utf-8')
mouse = Controller()
first_match = True
while True:

    # sct_img = ImageGrab.grab(bbox=bbox)

    img = ImageGrab.grab(bbox=bbox_ss)
    processed = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img)
    print(text)
    
    n_match = re.search("is ([0-9O|/\\]]+) in", text)

    if n_match:
        n_match = n_match.group(1).replace("O", "0").replace("|", "1").replace("/", "7").replace("]", "1")
        if first_match:
            first_match = False
            time.sleep(1)
            continue
        num = int(n_match)
        binary = bin(num)[2:].zfill(8)
        print(binary)

        #ydotool_run(["mousemove", "--", str(-button_x_delta), "0"])

        for i in range(8):
            bx, by = first_bit_s
            b_shifted = (bx + button_x_delta * i, by)


            if binary[i] == '1':
                ydotool_run(["click", "0x40", "0x80"])
            
            if i != 7:
                ydotool_run(["mousemove", "--", str(button_x_delta), "0"])
                time.sleep(0.25)

        for i in range(3):
            time.sleep(0.25)
            ydotool_run(["mousemove", "--", str(-button_x_delta - backwards_correction), "0"])

        ydotool_run(["mousemove", "--", "0", str(down)])
        ydotool_run(["click", "0x40", "0x80"])
        ydotool_run(["mousemove", "--", "0", str(-down - upwards_correction)])
        time.sleep(0.25)

        for i in range(4):
            time.sleep(0.25)
            ydotool_run(["mousemove", "--", str(-button_x_delta - backwards_correction), "0"])
        # ydotool_run(["mousemove", "--", str(submit_s[0]), str(submit_s[1])])
        # ydotool_run(["click", "0x40", "0x80"])
        # mouse.click(Button.left, 1)
    else:
        print("No match")

