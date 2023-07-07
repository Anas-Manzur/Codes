import cv2
import sys
from matplotlib import pyplot as plt


cascPath = "F:\\Research\\Project\\myhaar.xml"

clotCascade = cv2.CascadeClassifier(cascPath)

"""cap = cv2.VideoCapture(0)
t = True
while(t):
    ret, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    t = False

cap.release()
cv2.destroyAllWindows()"""

image = cv2.imread("F:\\Research\\Project\\Clots\\Dataset\\O-1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]

"""im_a = gray[100:200, 100:250]
im_b = gray[100:200, 250:420]
im_d = gray[100:200, 420:550]"""

clots = clotCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags=cv2.CASCADE_SCALE_IMAGE
)

for (x, y, w, h) in clots:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

a = 0
b = 0
d = 0

for (x, y, w, h) in clots:
    if x >= 100 and x <= 250:
        a = 1
    elif x > 250 and x <= 420:
        b = 1
    elif x > 420 and x <= 550:
        d = 1

if a == 0:
    blood = "A"
    if b == 0:
        blood = f"{blood}B"
elif b == 0:
    blood = "B"
else:
    blood = "O"

if d == 0:
    blood = f"{blood}+"
else:
    blood = f"{blood}-"

print("Blood Group is : "+blood)

cv2.imshow("img", image)
cv2.waitKey(0)
