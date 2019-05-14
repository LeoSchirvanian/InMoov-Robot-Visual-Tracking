#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  eyes.py
#
#  Copyright 2019 Unknown <bastien@mx-bastien>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

#Library
import numpy as np
import cv2 as cv
import control
import time


#'''
#Machine learning file
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

#Video capture object
cap = cv.VideoCapture(2)
cap1 = cv.VideoCapture(4)

#cap.read() returns a bool (True/False) frame by frame
#If frame is read correctly, it will be True
ret, frame = cap.read()

#Video dimension
cols,rows,colors = frame.shape
print("Dimension du flux video : " + str(rows) + "x" + str(cols))

#Main loop
while(cap.isOpened()):

    ret, frame = cap.read()
    img = frame

    ret1,frame1 = cap1.read()
    img1 = frame1

    #Color change
    #img = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    #frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    #Detects objects of different sizes in the input image.
    #The detected objects are returned as a list of rectangles. More...
    faces = face_cascade.detectMultiScale(frame, 1.2, 5)
    faces1 = face_cascade.detectMultiScale(frame1, 1.2, 5)

    #Initialization of center
    centre = []
    centre1 = []

    #Rectangle display
    #Rectangle = position(x,y) + dim(largeur,hauteur)

    #Detect only the largest face
    hmax = 0
    wmax = 0
    xmax = 0
    ymax = 0

    hmax1 = 0
    wmax1 = 0
    xmax1 = 0
    ymax1 = 0
    
    for (x,y,w,h) in faces :
        if(w*h > wmax*hmax):
            wmax = w
            hmax = h
            xmax = x
            ymax = y
            
    for (x,y,w,h) in faces1 :
        if(w*h > wmax1*hmax1):
            wmax1 = w
            hmax1 = h
            xmax1 = x
            ymax1 = y

    #Affiche centre du carré de(s) visage(s)
    #Display of center of faces
    hm = int(hmax / 2)
    wm = int(wmax / 2)
    #cv.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
    #cv.circle(img, (x+wm,y+hm), 5, (0, 0, 255), -1, 4)

    #Add faces center to the list
    if(not (hmax==0 or wmax==0 or xmax==0 or ymax==0)) :
        centre.append((xmax+wm,ymax+hm))

    #Affiche centre du carré de(s) visage(s)
    #Display of center of faces
    hm1 = int(hmax1 / 2)
    wm1 = int(wmax1 / 2)
    #cv.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
    #cv.circle(img, (x+wm,y+hm), 5, (0, 0, 255), -1, 4)

    #Add faces center to the list
    if(not (hmax1==0 or wmax1==0 or xmax1==0 or ymax1==0)) :
        centre1.append((xmax1+wm1,ymax1+hm1))
    
    #print(centre, centre1)

######################################################################################### ALL FACES ##############################################################################################################
    '''
    for (x,y,w,h) in faces:

        #Rectangle display for faces
        #cv.Rectangle(img, pt1, pt2, color, thickness=1, lineType=8, shift=0) → None
        #cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        #Affiche centre du carré de(s) visage(s)
        #Display of center of faces
        hm = int(h / 2)
        wm = int(w / 2)
        #cv.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        #cv.circle(img, (x+wm,y+hm), 5, (0, 0, 255), -1, 4)

        #Add faces center to the list
        centre.append((x+wm,y+hm))

        #cv.line(img, (x,y+hm), (x+w,y+hm), (0,0,255), 1)
        #cv.line(img, (x+wm,y), (x+wm,y+h), (0,0,255), 1)

        #Video cut
        #roi_gray = img[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)

        #Eyes rectangle display
        #for (ex,ey,ew,eh) in eyes:
            #ewm = int(ew / 2)
            #ehm = int(eh / 2)
            #centre.append([y+ey+ehm,ex,ey,ew,eh,ewm,ehm])
            #cv.rectangle(roi_gray,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
            #cv.circle(img, (x+ex+ewm,y+ey+ehm), 3, (0, 0, 255), -1, 4)
            #cv.line(img, (x+ex,y+ey+ehm), (x+ex+ew,y+ey+ehm), (0,0,255), 1)
            #cv.line(img, (x+ex+ewm,y+ey), (x+ex+ewm,y+ey+eh), (0,0,255), 1)right

    for (x,y,w,h) in faces1:

        #Rectangle display for faces
        #cv.Rectangle(img, pt1, pt2, color, thickness=1, lineType=8, shift=0) → None
        #cv.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)

        #Affiche centre du carré de(s) visage(s)
        #Display of center of faces
        hm = int(h / 2)
        wm = int(w / 2)
        #cv.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        #cv.circle(img, (x+wm,y+hm), 5, (0, 0, 255), -1, 4)

        #Add faces center to the list
        centre1.append((x+wm,y+hm))

        #cv.line(img1, (x,y+hm), (x+w,y+hm), (0,0,255), 1)
        #cv.line(img1, (x+wm,y), (x+wm,y+h), (0,0,255), 1)

        #Video cut
        #roi_gray = img[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)

        #Eyes rectangle display
        #for (ex,ey,ew,eh) in eyes:
            #ewm = int(ew / 2)
            #ehm = int(eh / 2)
            #centre.append([y+ey+ehm,ex,ey,ew,eh,ewm,ehm])
            #cv.rectangle(roi_gray,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
            #cv.circle(img, (x+ex+ewm,y+ey+ehm), 3, (0, 0, 255), -1, 4)
            #cv.line(img, (x+ex,y+ey+ehm), (x+ex+ew,y+ey+ehm), (0,0,255), 1)
            #cv.line(img, (x+ex+ewm,y+ey), (x+ex+ewm,y+ey+eh), (0,0,255), 1)
    '''
    #Detect where is the sum of the center on the video
    consigneX = 0
    consigneY = 0

    if len(centre) != 0 :
        gx = 0
        gy = 0
        for x in centre :
            gx += x[0]   #sum of length of faces center (x)
            gy += x[1]   #sum of width of faces center (y)
        gx = gx // len(centre)
        gy = gy // len(centre)
        distancex = abs(gx - rows//2)
        distancey = abs(gy - cols//2)
        #print(distancex, distancey, len(centre))
        cv.circle(img, (gx,gy), 5, (0, 0, 255), -1, 4)

        taux = 0.08
        consigneX = -int(taux*(gx-rows/2.0))
        consigneY = -int(taux*(gy-cols/2.0))


        #Display a circle of different color according to the position of the sum of the faces center
        #if gx > (2*rows/3) :    #Head on right => turn left
            #cv.circle(img, (50,50), 5, (255, 0, 0), -1, 4)
        #else :                    #Head on middle => don't do anything
            #cv.circle(img, (50,50), 5, (0, 0, 255), -1, 4)

    if len(centre1) != 0 :
        gx = 0
        gy = 0
        for x in centre1 :
            gx += x[0]   #sum of length of faces center (x)
            gy += x[1]   #sum of width of faces center (y)
        gx = gx // len(centre1)
        gy = gy // len(centre1)
        distancex = abs(gx - rows//2)
        distancey = abs(gy - cols//2)
        #print(distancex, distancey, len(centre))
        cv.circle(img1, (gx,gy), 5, (0, 0, 255), -1, 4)

        taux = 0.08
        consigneX2 = -int(taux*(gx-rows/2.0))
        consigneY2 = -int(taux*(gy-cols/2.0))

        if(abs(consigneX2) + abs(consigneY2)>abs(consigneX)+abs(consigneY)):
            consigneX = consigneX2
            consigneY = consigneY2

        #Display a circle of different color according to the position of the sum of the faces center
        #if gx > (2*rows/3) :    #Head on right => turn left
            #cv.circle(img1, (50,50), 5, (255, 0, 0), -1, 4)
        #else :                    #Head on middle => don't do anything
            #cv.circle(img1, (50,50), 5, (0, 0, 255), -1, 4)


##############################################################################################################################################################################################################

    

    time.sleep(0.016)
    control.update()

    #print(str(control.p)+","+str(control.t))

    if(control.isReady() and (consigneX!=0 or consigneY!=0)):
        control.regarde(consigneX,consigneY)

    #cv.imshow('right eyes',img)
    #if cv.waitKey(10) & 0xFF == ord('q'):  #Wait 10ms before next image display or quit if you press the 'q' key
    #    break

    #POUR AVOIR DEUX DANS UNE FENETRE :
    numpy_horizontal_concat = np.concatenate((img1, img), axis=1)

    cv.imshow('Robot view',numpy_horizontal_concat)
    if cv.waitKey(10) & 0xFF == ord('q'):  #Wait 10ms before next image display or quit if you press the 'q' key
        break

#When everything is done, release the capture
cap.release()
cap1.release()
cv.destroyAllWindows()
#'''

'''
cams_test = 99
for i in range(0, cams_test):
    cap = cv.VideoCapture(i)
    test, frame = cap.read()
    print("i : "+str(i)+" /// result: "+str(test))'''
