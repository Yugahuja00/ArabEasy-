# -*- coding: utf-8 -*-
"""
Created on Thu May 27 06:30:05 2021

@author: Lenovo
"""
import cv2
import numpy as np
from time import sleep

l_min=80 
a_min=80 

offset=6  

pos_l=550 

delay= 60

detec = []
car= 0

	
def pega_centre(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('video.mp4')
sub = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret , frame1 = cap.read()
    tempo = float(1/delay)
    sleep(tempo) 
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    img_sub = sub.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    detectt = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    detectt = cv2.morphologyEx (detectt, cv2. MORPH_CLOSE , kernel)
    contorno,h=cv2.findContours(detectt,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1, (25, pos_l), (1200, pos_l), (255,127,0), 3) 
    for(i,c) in enumerate(contorno):
        (x,y,w,h) = cv2.boundingRect(c)
        val = (w >= l_min) and (h >= a_min)
        if not val:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)        
        centre = pega_centre(x, y, w, h)
        detec.append(centre)
        cv2.circle(frame1, centre, 4, (0, 0,255), -1)

        for (x,y) in detec:
            if y<(pos_l+offset) and y>(pos_l-offset):
                car+=1
                cv2.line(frame1, (25, pos_l), (1200, pos_l), (0,127,255), 3)  
                detec.remove((x,y))
                print("car is detected : "+str(car))        
       
    cv2.putText(frame1, "VEHICLE COUNT : "+str(car), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("Video Original" , frame1)
    cv2.imshow("Detector",detectt)

    key = cv2.waitKey(1) & 0xFF
    if key==ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
