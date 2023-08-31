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
button_x_delta = 100
submit = (962, 1030)
submit_s = (962 + dx, 1030)

def ydotool_run(args):
    print(" ".join(["ydotool"] + args))
    return subprocess.run(["ydotool"] + args, stdout=subprocess.PIPE).stdout.decode('utf-8')
mouse = Controller()
while True:

    # sct_img = ImageGrab.grab(bbox=bbox)

    img = ImageGrab.grab(bbox=bbox_ss)
    img.save("screen.png")
    # cv2.imshow('screen', np.array(img))
    cropped = img
    text = pytesseract.image_to_string(cropped)
    text = text.replace("|", "1")
    print(text)

    n_match = re.search("is (\\d+) in", text)

    if n_match:
        num = int(n_match.group(1))
        binary = bin(num)[2:].zfill(8)
        print(binary)
        for i in range(8):
            bx, by = first_bit_s
            b_shifted = (bx + button_x_delta * i, by)

            if binary[i] == '1':
                ydotool_run(["mousemove", "-a", "--", str(b_shifted[0]), str(b_shifted[1])])
                ydotool_run(["click", "0x40", "0x80"])
                time.sleep(1)

        ydotool_run(["mousemove", "-a", "--", str(submit_s[0]), str(submit_s[1])])
        ydotool_run(["click", "0x40", "0x80"])
        # mouse.click(Button.left, 1)
        break

    else:
        print("No match")

