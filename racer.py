#!/usr/bin/env python3

import numpy as np
import cv2
import pyscreenshot as ImageGrab
import pytesseract
from PIL import Image
import re

while True:
    bbox = (800, 480, 1180, 580)
    x1, y1, x2, y2 = bbox
    bbox_s = (x1 + 1920, y1, x2 + 1920, y2)
    # sct_img = ImageGrab.grab(bbox=bbox)

    img = ImageGrab.grab()
    img.save("screen.png")
    # cv2.imshow('screen', np.array(img))
    cropped = img.crop(bbox_s)
    processed = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(processed)
    text = text.replace("|", "1")
    print(text)

    match = re.search("is (\\d+) in", text)

    if match:
        num = int(match.group(1))
        binary = bin(num)[2:].zfill(8)
        print(binary)
    else:
        print("No match")