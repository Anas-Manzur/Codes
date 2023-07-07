# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 23:12:12 2018

@author: MY PC
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 00:00:18 2018

@author: MY PC
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 15:28:30 2018

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

directory_template = "G:\\workspace\\opencv\\project\\biomed project"
gray_path = directory_template + "\\gray"
if not os.path.exists(gray_path):
    os.makedirs(gray_path)

w = 1000
h = 1000
resized_image = np.zeros((w,h,3))

original_path = directory_template + "\\binary"
resized_path = directory_template + "\\resizedbinary"
if not os.path.exists(resized_path):
    os.makedirs(resized_path)
    
original_files = os.listdir(original_path)    
for original_filename in original_files:
    gray_img = cv2.imread(os.path.join(original_path,original_filename),0)
    cv2.imwrite(os.path.join(gray_path , original_filename), gray_img)
    original_img = cv2.imread(os.path.join(original_path,original_filename))
    oheight, owidth, ochannels = original_img.shape
    #print("shape of " + original_filename + ": " + str(owidth) + " X " + str(oheight) + " channels: " + str(ochannels))
    resized_image = cv2.resize(original_img, dsize=(w, h), interpolation=cv2.INTER_CUBIC) 
    rheight, rwidth, rchannels = resized_image.shape
    #print("resized shape of " + original_filename + ": " + str(rwidth) + " X " + str(rheight) + " channels: " + str(rchannels))
    resized_image_name = 'reshaped' + original_filename
    #print(resized_image_name)
    cv2.imwrite(os.path.join(resized_path , resized_image_name), resized_image)
    

#%% source1 aka otsu thresholding 

noise_free_binary_path1 = directory_template + "\\noisefreebinary1"
if not os.path.exists(noise_free_binary_path1):
    os.makedirs(noise_free_binary_path1)
    
noise_free1_files = os.listdir(resized_path)
for noise_free1_filename in noise_free1_files:
    #print(noise_free1_filename)
    gray_img = cv2.imread(os.path.join(resized_path,noise_free1_filename),0)
    cv2.imwrite(os.path.join(gray_path , original_filename), gray_img)
    graynf1_img = cv2.imread(os.path.join(resized_path,noise_free1_filename),0)
    ret1,nf1 = cv2.threshold(graynf1_img,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    nf1_filename = 'nf1'+ noise_free1_filename
    cv2.imwrite(os.path.join(noise_free_binary_path1  , nf1_filename), nf1)
    #print(nf1_filename)
    
#%% erosion -> dialation -> opening -> closing -> smoothing

deoc = directory_template + "\\DialationErosionOpeningClosing"
if not os.path.exists(deoc):
    os.makedirs(deoc)
deocfiles = os.listdir(noise_free_binary_path1)
for deocfilename in deocfiles:
    deocimg = cv2.imread(os.path.join(noise_free_binary_path1,deocfilename))
    #print(deocimg.shape)
    kernel = np.ones((3,3),np.uint8)
    erosion1 = cv2.erode(deocimg,kernel,iterations = 1)
    dilation1 = cv2.dilate(erosion1,kernel,iterations = 1)
    opening1 = cv2.morphologyEx(dilation1, cv2.MORPH_OPEN, kernel)
    closing1 = cv2.morphologyEx(opening1, cv2.MORPH_CLOSE, kernel)
    smoothing1 = cv2.GaussianBlur(closing1,(3,3),0)
    deocfilenm = 'deoc'+ deocfilename[11:]
    cv2.imwrite(os.path.join(deoc , deocfilenm), smoothing1)
    #print(deocfilenm)
    
    
#%% gaussian noise free 

source  = resized_path
destination = directory_template + "\\noisefreebinary2"
if not os.path.exists(destination):
    os.makedirs(destination)
    
nf2files = os.listdir(source )
for nf2filename in nf2files:
    nf2img = cv2.imread(os.path.join(source ,nf2filename))
    graynf2img = cv2.imread(os.path.join(source ,nf2filename),0)
    blur2 = cv2.GaussianBlur(graynf2img,(3,3),0)
    th2 = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,2)
    kernel2 = np.ones((3,3),np.uint8)
    erosion2 = cv2.erode(th2,kernel2,iterations = 1)
    dilation2 = cv2.dilate(erosion2,kernel2,iterations = 1)
    opening2 = cv2.morphologyEx(dilation2, cv2.MORPH_OPEN, kernel2)
    closing2 = cv2.morphologyEx(opening2, cv2.MORPH_CLOSE, kernel2)
    smoothing2 = cv2.GaussianBlur(closing2,(3,3),0)
    nf2filenm = 'nf2'+ nf2filename
    cv2.imwrite(os.path.join(destination , nf2filenm), smoothing2)
    
#%% XOR aka combining image for quantization

source1  = deoc
source2  = destination
destination2 = directory_template + "\\combined"
if not os.path.exists(destination2):
    os.makedirs(destination2)
    
sourceone = []
sourcetwo = []

files1 = os.listdir(source1)
for filename1 in files1:
    sourceone.append(filename1)
    
files2 = os.listdir(source2)
for filename2 in files2:
    sourcetwo.append(filename2)   
 
length1 = len(sourceone)
length2 = len(sourcetwo)

#print("sourceone: ",str(length1),end='\n')
#print(sourceone,end='\n')
#print("sourcetwo: ",str(length2),end='\n')
#print(sourcetwo,end='\n')

for i in range(0,length1,1):
    s1 = sourceone[i]
    s2 = sourcetwo[i]
    imgs1 = s1[4:]
    imgs2 = s2[11:]
    if (imgs1 == imgs2):
        imgxor1 = cv2.imread(os.path.join(source1 ,s1),0)
        imgxor2 = cv2.imread(os.path.join(source2 ,s2),0)
        xlength,ylength = imgxor1.shape
        imgxor3 = np.zeros((xlength,ylength))
        imgxor1 = 255-imgxor1
        imgxor2 = 255-imgxor2
        imgxor3 = imgxor1-imgxor2
        kernel = np.ones((5,5),np.uint8)
        imgxor3 = cv2.morphologyEx(imgxor3, cv2.MORPH_OPEN, kernel)
        retxor, imgxor3 = cv2.threshold(imgxor3,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        imgxor3 = 255-imgxor3

    combinedname =  imgs1
    cv2.imwrite(os.path.join(destination2 , combinedname),imgxor3)
    #print(combinedname)


destination3 = "G:\\workspace\\opencv\\project\\biomed project\\detectbox"
if not os.path.exists(destination3):
    os.makedirs(destination3)
destination4 = "G:\\workspace\\opencv\\project\\biomed project\\seperate"
if not os.path.exists(destination4):
    os.makedirs(destination4)
shutil.rmtree(destination4)
if not os.path.exists(destination4):
    os.makedirs(destination4)
source3 = "G:\\workspace\\opencv\\project\\biomed project\combined"
classification_string = ""
loadfiles = os.listdir(source3 )
for loadfilename in loadfiles:
    load = cv2.imread(os.path.join(source3 ,loadfilename),0)
    
    w = 1000
    h = 1000
    imgload = np.random.random([w, h])
    imgload = load
# =============================================================================
#     for i in range (0,w-1,1):
#       for j in range (0,h-1,1):  
#           if(imgload[i,j] == 0):
#               top = i
#     for i in range (w-1,0,-1):
#       for j in range (0,h-1,1):  
#           if(imgload[i,j] == 0):
#               bottom = i
#     print(top)
#     print(bottom)
#     
#     for j in range (0,h-1,1):
#       for i in range (0,w-1,1):  
#           if(imgload[i,j] == 0):
#               right = j
#     for j in range (h-1,0,-1):
#       for i in range (0,w-1,1):  
#           if(imgload[i,j] == 0):
#               left = j
#     print(left)
#     print(right)
#     
#     xdistance = abs(left-right)
#     ydistance = abs(top-bottom)
# =============================================================================
    white = 0
    dark = 0
    for i in range (0,w-1,1):
        for j in range (0,h-1,1):
            if(imgload[i,j] == 0):
              dark = dark + 1
            elif(imgload[i,j] == 255) :
                white = white + 1
    print("dark = ", str(dark), end = '\t')
    print("white = ", str(white))      
    ratio = dark/white
    print(loadfilename +"percentage = " + str(ratio))
   
        
