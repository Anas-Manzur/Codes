# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 01:13:21 2018

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

im = cv2.imread("jersey.jpg")
# define range of blue color in HSV
im[np.where((im == [255,255,255]).all(axis = 2))] = [0,0,0]
cv2.imwrite('output.png', im)
                

if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.destroyAllWindows()