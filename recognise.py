import numpy as np
import cv2
import math
from quadcopter import Drone

face_cascade = cv2.CascadeClassifier('harrarface.xml')

cap = cv2.VideoCapture(0)

req_area = 24649 #specific to my xml file
threshold = 10

screen_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
screen_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
screen_center = (int(round(screen_width//2)), int(round(screen_height//2)))

print("Center OF screen is", screen_center)


input("start?")

drone = Drone()
drone.calibrate()
while 1:
    if process:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.6, 5)

        for (x,y,w,h) in faces[0]:
            area = w*w
            if area == req_area:
                fc_x = int(x+w//2)
                fc_y = int(y+h//2)

                move_x = screen_center[0]-fc_x
                move_y = screen_center[1]-fc_y


                if move_x >= threshold:
                    #turn right
                    drone.control('e')
                elif move_x <= -threshold:
                    #turn left
                    drone.control('q')
                else:
                    print("no x")

                if move_y >= threshold:
                    #go up 
                    drone.control('r')
                elif move_y <= -threshold:
                    #go down
                    drone.control('f')
                else:
                    print("no y")

                if area < req_area:
                    #go_forward()
                    drone.control('w')
                elif area > req_area:
                    #go_backwards()
                    drone.control('s')


            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.circle(img, target_center, 5,(255,0,0),2)
            cv2.circle(img, actual_center, 5,(0,255,0),2)
        cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
