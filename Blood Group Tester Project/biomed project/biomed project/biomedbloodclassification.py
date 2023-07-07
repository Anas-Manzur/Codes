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
mainbinary_path = directory_template + "\\binary"
main_path = directory_template + "\\main file"
if not os.path.exists(mainbinary_path):
    os.makedirs(mainbinary_path)
    

# original_filename = input("enter the original image name:  ")
original_filename = "4.JPG"    
original_img = cv2.imread(os.path.join(main_path,original_filename))
mheight, mwidth, mchannels = original_img.shape
print("main file shape is " + original_filename + ": " + str(mwidth) + " X " + str(mheight) + " channels: " + str(mchannels))


# Cut the image in 4 pieces
img = misc.imread(os.path.join(main_path,original_filename))
height, width, _ = img.shape

width_cutoff = width //4 
s1 = img[:, :width_cutoff, :]
s2 = img[:, width_cutoff:2*width_cutoff, :]
s3 = img[:, 2*width_cutoff:3*width_cutoff, :]
s4 = img[:, 3*width_cutoff:, :]
# Save each one

misc.imsave(os.path.join(mainbinary_path , "A.jpg"), s1)
misc.imsave(os.path.join(mainbinary_path , "B.jpg"), s2)
misc.imsave(os.path.join(mainbinary_path , "AB.jpg"), s3)
misc.imsave(os.path.join(mainbinary_path , "Rh.jpg"), s4)


w = 1000
h = 1000
resized_image = np.zeros((w,h,3))

original_path = directory_template + "\\binary"
resized_path = directory_template + "\\resizedbinary"
if not os.path.exists(resized_path):
    os.makedirs(resized_path)
    
original_files = os.listdir(original_path)    
for original_filename in original_files:
    original_img = cv2.imread(os.path.join(original_path,original_filename))
    oheight, owidth, ochannels = original_img.shape
    print("shape of " + original_filename + ": " + str(owidth) + " X " + str(oheight) + " channels: " + str(ochannels))
    resized_image = cv2.resize(original_img, dsize=(w, h), interpolation=cv2.INTER_CUBIC) 
    rheight, rwidth, rchannels = resized_image.shape
    print("resized shape of " + original_filename + ": " + str(rwidth) + " X " + str(rheight) + " channels: " + str(rchannels))
    resized_image_name = 'reshaped' + original_filename
    print(resized_image_name)
    cv2.imwrite(os.path.join(resized_path , resized_image_name), resized_image)
    

#%% source1 aka otsu thresholding 

noise_free_binary_path1 = directory_template + "\\noisefreebinary1"
if not os.path.exists(noise_free_binary_path1):
    os.makedirs(noise_free_binary_path1)
    
noise_free1_files = os.listdir(resized_path)
for noise_free1_filename in noise_free1_files:
    print(noise_free1_filename)
    graynf1_img = cv2.imread(os.path.join(resized_path,noise_free1_filename),0)
    ret1,nf1 = cv2.threshold(graynf1_img,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    nf1_filename = 'nf1'+ noise_free1_filename
    cv2.imwrite(os.path.join(noise_free_binary_path1  , nf1_filename), nf1)
    print(nf1_filename)
    
#%% erosion -> dialation -> opening -> closing -> smoothing

deoc = directory_template + "\\DialationErosionOpeningClosing"
if not os.path.exists(deoc):
    os.makedirs(deoc)
deocfiles = os.listdir(noise_free_binary_path1)
for deocfilename in deocfiles:
    deocimg = cv2.imread(os.path.join(noise_free_binary_path1,deocfilename))
    print(deocimg.shape)
    kernel = np.ones((3,3),np.uint8)
    erosion1 = cv2.erode(deocimg,kernel,iterations = 1)
    dilation1 = cv2.dilate(erosion1,kernel,iterations = 1)
    opening1 = cv2.morphologyEx(dilation1, cv2.MORPH_OPEN, kernel)
    closing1 = cv2.morphologyEx(opening1, cv2.MORPH_CLOSE, kernel)
    smoothing1 = cv2.GaussianBlur(closing1,(3,3),0)
    deocfilenm = 'deoc'+ deocfilename[11:]
    cv2.imwrite(os.path.join(deoc , deocfilenm), smoothing1)
    print(deocfilenm)
    
    
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

print("sourceone: ",str(length1),end='\n')
print(sourceone,end='\n')
print("sourcetwo: ",str(length2),end='\n')
print(sourcetwo,end='\n')

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

    combinedname = 'combo'+ imgs1
    cv2.imwrite(os.path.join(destination2 , combinedname),imgxor3)
    print(combinedname)


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

arealst = []
allarealst = []

circlearea = []
allcirclearea = []

circlecenter = []
circleradius = []
allcirclecenter = []
allcircleradius = []
combofiles = os.listdir(source3)
for combofilename in combofiles:
    imgprint = cv2.imread(os.path.join(source3 ,combofilename))
    img1 = cv2.imread(os.path.join(source3 ,combofilename),0)
    img2 = cv2.Canny(img1,0,255)
    im1, contours, hierarchy = cv2.findContours(img2,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# =============================================================================
# photo = 'comboB15.jpg'
# imgprint = cv2.imread(photo)
# img1 = cv2.imread(photo,0)
# img2 = cv2.Canny(img1,0,255)
# im1, contours, hierarchy = cv2.findContours(img2,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# =============================================================================
    print("in " + combofilename + " no of contours: " + str(len(contours)))
    boxcount = 0
    for i in range (0,len(contours),1):
        cnt = contours[i]
        M = cv2.moments(cnt)
        #print(cnt)
        #area = cv2.contourArea(cnt)
        #print("area: " , str(area))
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        
        x,y,w,h = cv2.boundingRect(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if (float(cv2.contourArea(cnt)) >= 30.0):
            im3 = cv2.circle(imgprint,center,radius,(0,0,0),3)
            arealst.append(float(cv2.contourArea(cnt)))
            circlecenter.append(center )
            circleradius.append(radius)
            circlearea.append(pi*radius**2)
            boxcount += 1
    
                
# image3 = cv2.rectangle(image1,(x,y),(x+w,y+h),(0,0,255),9)
    print(combofilename + " box count: " + str(boxcount))       
    if (boxcount >= 7):
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        seperatefilename = "1" + combofilename[5:]
        cv2.imwrite(os.path.join(destination4 , seperatefilename),imgprint)
        
    elif (boxcount < 7):
        print("NNNNNNNNNNNNNNNNNNNNNNNNN")
        seperatefilename = "0" + combofilename[5:]
        cv2.imwrite(os.path.join(destination4 , seperatefilename),imgprint)
        
    
    #print("area of " + combofilename , end = '\t')
    #print(allarealst)
    #print(circlearea)
    #print(circlecenter)
    #print(circleradius)
# =============================================================================
#     print("avrg of " + combofilename , end = '\t')
#     print(np.mean(arealst))
#     print("max of " + combofilename , end = '\t')
#     print(np.amax(arealst))
# =============================================================================
    allarealst.append(arealst)
    allcirclecenter.append(circlecenter)
    allcircleradius.append(circleradius)
    allcirclearea.append(circlearea)
    #allboxarea.append(boxarea)
    #allboxcoordinate.append(boxcoordinate)
    
    arealst[:] = []
    circlecenter[:] = []
    circleradius[:] = []
    circlearea[:] = []
    newname = 'check' + combofilename
    cv2.imwrite(os.path.join(destination3 , newname),im3) 
    
#%% final    
savefilename = "O"
destination5 = "G:\\workspace\\opencv\\project\\biomed project\\final save"
if not os.path.exists(destination5):
    os.makedirs(destination5)
destination4 = "G:\\workspace\\opencv\\project\\biomed project\\seperate"
checkfiles = os.listdir(destination4)
for checkfilename in checkfiles:
    if(checkfilename == "1A.jpg"):
        savefilename = savefilename+ "A"
    if(checkfilename == "1B.jpg"):
        savefilename = savefilename+ "B"
    if(checkfilename == "1Rh.jpg"):
        savefilename = savefilename+ " positive"
    if(checkfilename == "0Rh.jpg"):
        savefilename = savefilename+ " negative" 
if(savefilename[1]!= " "):
   savefilename = savefilename[1:] 
   
# =============================================================================
# save_img = misc.imread(os.path.join(main_path,original_filename))
# savefilename  = savefilename + ".JPG"
# cv2.imwrite(os.path.join(destination5, savefilename), save_img) 
# =============================================================================
print(savefilename)
print()

