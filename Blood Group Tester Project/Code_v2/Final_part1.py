import serial
import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)

ser1 = serial.Serial("COM3", 9600)

a, pbg = cv2.VideoCapture(1)
pbg.release()
cv2.destroyAllWindows()
ser1.write("A".encode())
image = cv2.imread("F:\\Research\\Project\\Clots\\Dataset\\A+91.jpg")
print(image)

while(False):
    b, pim = cv2.VideoCapture(1)
    for i in pbg:
        for j in i:
            for k in j:
