import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)

"""cap = cv2.VideoCapture(0)

while(True):
    ret, image = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""

image = cv2.imread("F:\\Research\\Project\\Clots\\Dataset\\A+91.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
bw = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)[1]


def ratio(img):
    nw = 0
    nb = 0

    for j in img:
        for i in j:
            if i > 0:
                nw = nw+1
            else:
                nb = nb+1
    return (nb/(nb+nw))*100


"""x = 0
y = 0
l = 1
k = 1
for i in bw:
    l = 1
    for j in i:
        if j > 0:
            x, y = l, k
            break
        l = l+1
    if(x > 0 and y > 0):
        break
    k = k+1

print(x, y)"""

im_a = bw[150:340, 6:213]
im_b = bw[150:340, 213:420]
im_d = bw[150:340, 420:627]

"""print(ratio(im_a), ratio(im_b), ratio(im_d))"""
group = "a"
if ratio(im_a) > 5:
    group = "A"
    if ratio(im_b) > 5:
        group = f"{group}B"
elif ratio(im_b) > 5:
    group = "B"

if ratio(im_d) > 5:
    group = f"{group}+"
else:
    group = f"{group}-"

result = "The Blood group is : "+group


image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image)
plt.show()
plt.imshow(bw)
plt.show()
plt.subplot(1, 3, 1)
plt.imshow(im_a)
plt.subplot(1, 3, 2)
plt.imshow(im_b)
plt.subplot(1, 3, 3)
plt.imshow(im_d)
plt.show()
plt.imshow(image)
plt.text(200, 400, result, bbox=dict(facecolor="white"))
plt.show()
