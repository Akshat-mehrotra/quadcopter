import numpy as np
import cv2
import math
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

face_cascade = cv2.CascadeClassifier('harrarface.xml')

cap = cv2.VideoCapture(0)

process = True
base = 10
delta = 10
req_area = 24649
threshold = 110

actual_center = (int(base*round((cap.get(cv2.CAP_PROP_FRAME_WIDTH)//2)/base)), int(base*round((cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//2)/base))) #(320, 240)
print(actual_center)

target_center = (0,0)

def move_z(rev=1):
    print(3*rev)

def move_y(rev=1, rapid=False):
    print(2*rev)

def move_x(rev=1, rapid=False):
    print(1*rev)

while 1:
    if process:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.6, 5)

        for (x,y,w,h) in faces:
            area = w*w
            if area == req_area:
                new_x = int(x+w//2)
                corrected_x = base*round(new_x/base) # rounding to the nearest base th multiple
                new_y = int(y+h//2)
                corrected_y = base*round(new_y/base)

                corrected_deltax = abs(corrected_x-target_center[0])
                corrected_deltay = abs(corrected_y-target_center[1])

                if corrected_deltax >= delta or corrected_deltay >= delta:
                    target_center = (corrected_x, corrected_y)

                move =  (target_center[0]-actual_center[0], actual_center[1]-target_center[1])


                if move[0] >= threshold:
                    move_x(rev=-1, rapid=True)
                elif move[0] <= -threshold:
                    move_x(rapid=True)
                else:
                    print("no x")
                if move[1] >= threshold:
                    move_y(rev=-1, rapid=True)
                elif move[1] <= -threshold:
                    move_y(rapid=True)
                else:
                    print("no y")

            elif area < req_area:
                move_z()
            elif area > req_area:
                move_z(-1)

            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.circle(img, target_center, 5,(255,0,0),2)
            cv2.circle(img, actual_center, 5,(0,255,0),2)
        cv2.imshow('img',img)
    process=not process
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
