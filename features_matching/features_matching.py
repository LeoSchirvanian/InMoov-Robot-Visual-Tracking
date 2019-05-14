import numpy as np
import cv2 as cv
import time
import io
import matplotlib.pyplot as plt

cap = cv.VideoCapture(0)
ret, frame = cap.read()
cols,rows,colors = frame.shape
print("Dimension du flux video : " + str(rows) + "x" + str(cols))


def get_box(matches,keysPoints) :
    west,east,north,south = 10000,0,10000,0
    for m in matches :
        x,y = keysPoints[m.trainIdx].pt
        if x<west : west = x
        if x>east : east = x
        if y<north : north = y
        if y>south : south = y
    return (int(west),int(east),int(north),int(south))




img1 = cv.imread('obj.png',0) # Image de reference



def get_matches(frame,nbPoints):
	global kp1
	orb = cv.ORB_create(nbPoints) # Descripteur de points
	kp1, des1 = orb.detectAndCompute(img1,None) # Description de l'image de reference
	kp2, des2 = orb.detectAndCompute(frame,None)
	bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
	matches = bf.match(des1,des2)
	matches = sorted(matches, key = lambda x:x.distance)
	return matches[:20],kp2
    


# Draw first 10 matches.

cv.imshow("Features Matching",img1)

nbPoints = 500
txt = ""

while(1):
	
	global kp1
	ret, frame = cap.read()
	frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
	t = time.time()
	matches,kp = get_matches(frame,nbPoints)
	txt += "("+str(nbPoints)+","+str(1000*(time.time()-t))+")"
	rect = get_box(matches,kp)
	
	cv.rectangle(frame,(rect[0],rect[2]), (rect[1],rect[3]), (0,0,0),2)
	
	img3 = cv.drawMatches(img1,kp1,frame,kp,matches,outImg=None, flags=2)
	
	cv.imshow('image',img3)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cv.destroyAllWindows()
print(txt)
