import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
from PIL import Image

name = glob.glob("F:\\Research\\Project\\Clots\\Dataset\\*.jpg")

i = 0

for filename in name:
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]
    path = f"F:\\Research\\Project\\Clots\\Gray\\obtbw\\image{i}.bmp"
    cv2.imwrite(path, image)
    i = i+1
