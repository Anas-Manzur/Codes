# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 20:58:07 2018

@author: MY PC
"""

import cv2
import numpy as np
import scipy as sp
import os
from math import pi
from scipy import misc
import sys
import shutil

w = 1000
h = 1000

imgload = cv2.imread("comboAB.jpg",0)

for i in range (0,w-1,1):
  for j in range (0,h-1,1):  
      if(imgload[i,j] == 0):
          top = i
for i in range (w-1,0,-1):
  for j in range (0,h-1,1):  
      if(imgload[i,j] == 0):
          bottom = i
print(top)
print(bottom)

for j in range (0,h-1,1):
  for i in range (0,w-1,1):  
      if(imgload[i,j] == 0):
          right = j
for j in range (h-1,0,-1):
  for i in range (0,w-1,1):  
      if(imgload[i,j] == 0):
          left = j
print(left)
print(right)

xdistance = abs(left-right)
ydistance = abs(top-bottom)
white = 0
dark = 0
for i in range (bottom,top,1):
    for j in range (left,right,1):
        if(imgload[i,j] == 0):
          dark = dark + 1
        elif(imgload[i,j] == 255) :
            white = white + 1
print("dark = ", str(dark), end = '\t')
print("white = ", str(white))      
ratio = dark/white
print("percentage = " + str(ratio))