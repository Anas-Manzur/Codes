import cv2
import sys
from matplotlib import pyplot as plt

cascPath = "F:\\Research\\Project\\Code\\myhaar.xml"

clotCascade = cv2.CascadeClassifier(cascPath)

"""cap = cv2.VideoCapture(0)

while(True):
    ret, image = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""

image = cv2.imread("F:\\Research\\Project\\Code\\Ave.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

"""im_a = gray[100:200, 100:250]
im_b = gray[100:200, 250:420]
im_d = gray[100:200, 420:550]"""

clots = clotCascade.detectMultiScale(
    image,
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

plt.imshow(image)
plt.show()
