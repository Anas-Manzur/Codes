import cv2
import numpy as np

image = cv2.imread("F:\\Research\\Project\\Ave.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

con1, hierarchy = cv2.findContours(
    gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print(con1)

for pic1, contour1 in enumerate(con1):
    area = cv2.contourArea(contour1)
    x, y, w, h = cv2.boundingRect(contour1)
    imgn1 = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
cv2.imshow("img", gray)
cv2.waitKey(0)
