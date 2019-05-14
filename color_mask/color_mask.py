#!/usr/bin/env python

#Library
import numpy as np
import cv2
import time

#Video capture object
cap = cv2.VideoCapture(0)  #4 for the robot
#cap.read() returns a bool (True/False) frame by frame
#If frame is read correctly, it will be True

ret, frame = cap.read()

cols,rows,colors = frame.shape
print(str(rows) + "x" + str(cols))

#Video dimension
cols,rows,colors = frame.shape
print("Dimension du flux video : " + str(rows) + "x" + str(cols))

#Do nothing
def nothing(x):
    pass

# Control to create a mask
cv2.namedWindow('image')
cv2.createTrackbar('HueLower','image',150,360, nothing)
cv2.createTrackbar('HueUpper','image',160,360, nothing)

#Initialization
upperH = 50
lowerH = 0

timeMoy = [] #time test

#Main loop
while(cap.isOpened):

    # Capture frame-by-frame
    ret, frame = cap.read()
    # HSV conversion
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definition of the border of the mask
    lowerH = cv2.getTrackbarPos('HueLower','image')         #Face detection => 5
    upperH = lowerH +cv2.getTrackbarPos('HueUpper','image') #Face detection => 5
    lower = np.array([lowerH, 100, 100])
    upper = np.array([upperH, 255, 255])

    debut = time.time()
    # Extract the mask
    mask = cv2.inRange(hsv, lower, upper)

    # Structurant element for morphological operations 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)) #25,25

    # Closure of morphological mask
    opening = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Extraction of mask borders
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ################################################ THRESHOLD POINTS CLUSTERS METHOD ########################################################
    '''
    #We only keep the most important cluster, with the most number of points in it
    if len(contours) != 0 :
    	mini = 300
	minCluster = []

	for clusters in contours :
		compt = 0
		for points in clusters :
			compt += 1
		if compt > mini :
			minCluster.append(clusters)
		
	#print(mini)
	#print(minCluster)
	
    #If we detect some shapes
    if len(minCluster) != 0 :

        #Initialization
        gx = 0
        gy = 0
        compt = 0  #count the number of point detected

        #Contours is a list which contains some clusters, each cluster contains a certain number of points
        #Our goal is too sum all the details of each point, add it, and calculate the mean and display it with a circle
        for clusters in minCluster:
            for points in clusters :
                gx += points[0,0]   #sum of length of a point center (x)
                gy += points[0,1]   #sum of width of a point center (y)
                compt += 1

        #The length and width mean        
        xx = gx // compt
        yy = gy // compt

        #Distance between x and y mean and the center of the image
        distancex = abs(xx - rows//2)
        distancey = abs(yy - cols//2)

        #Display a circle which represents the mean of all the points
        cv2.circle(frame, (xx,yy), 5, (0, 0, 255), -1, 4)

        #Display a circle of different color according to the position of the mean circle 
        if xx < (rows/3) :        #Head on left => turn right
            cv2.circle(frame, (50,50), 5, (0, 255, 0), -1, 4)
        elif xx > (2*rows/3) :    #Head on right => turn left
            cv2.circle(frame, (50,50), 5, (255, 0, 0), -1, 4)
        else :                    #Head on middle => don't do anything
            cv2.circle(frame, (50,50), 5, (0, 0, 255), -1, 4)
	

        #print(compt)
    #We draw a contours with the points we have detected
    cv2.drawContours(frame, minCluster, -1, (0, 255, 0), 3)
    '''

    ############################################ ONLY WITH THE GREATEST CLUSTER DETECTION ####################################################

    '''
    #We only keep the most important cluster, with the most number of points in it
    if len(contours) != 0 :
    	maxi = 0
    	ind = 0
	for clusters in contours :
		compt = 0
		for points in clusters :
			compt += 1
		if compt > maxi :
			maxi = compt
			indi = clusters

	#print(maxi,indi)
	
	maxCluster = []
	maxCluster.append(indi)
	#print(maxCluster)
	
    #If we detect some shapes
    if len(maxCluster) != 0 :

        #Initialization
        gx = 0
        gy = 0
        compt = 0  #count the number of point detected

        #Contours is a list which contains some clusters, each cluster contains a certain number of points
        #Our goal is too sum all the details of each point, add it, and calculate the mean and display it with a circle
        for clusters in maxCluster:
            for points in clusters :
                gx += points[0,0]   #sum of length of a point center (x)
                gy += points[0,1]   #sum of width of a point center (y)
                compt += 1

        #The length and width mean        
        xx = gx // compt
        yy = gy // compt

        #Distance between x and y mean and the center of the image
        distancex = abs(xx - rows//2)
        distancey = abs(yy - cols//2)

        #Display a circle which represents the mean of all the points
        cv2.circle(frame, (xx,yy), 5, (0, 0, 255), -1, 4)

        #Display a circle of different color according to the position of the mean circle 
        if xx < (rows/3) :        #Head on left => turn right
            cv2.circle(frame, (50,50), 5, (0, 255, 0), -1, 4)
        elif xx > (2*rows/3) :    #Head on right => turn left
            cv2.circle(frame, (50,50), 5, (255, 0, 0), -1, 4)
        else :                    #Head on middle => don't do anything
            cv2.circle(frame, (50,50), 5, (0, 0, 255), -1, 4)
	

        #print(compt)
    #We draw a contours with the points we have detected
    cv2.drawContours(frame, maxCluster, -1, (0, 255, 0), 3)
    '''

    ########################################## ALL DETECTION ################################################

    
    #If we detect some shapes
    if len(contours) != 0 :

        #Initialization
        gx = 0
        gy = 0
        compt = 0  #count the number of point detected

        #Contours is a list which contains some clusters, each cluster contains a certain number of points
        #Our goal is too sum all the details of each point, add it, and calculate the mean and display it with a circle
        for clusters in contours:
            for points in clusters :
                gx += points[0,0]   #sum of length of a point center (x)
                gy += points[0,1]   #sum of width of a point center (y)
                compt += 1

        #The length and width mean        
        xx = gx // compt
        yy = gy // compt

        #Distance between x and y mean and the center of the image
        distancex = abs(xx - rows//2)
        distancey = abs(yy - cols//2)

        #Display a circle which represents the mean of all the points
        cv2.circle(frame, (xx,yy), 5, (0, 0, 255), -1, 4)

        #Display a circle of different color according to the position of the mean circle 
        if xx < (rows/3) :        #Head on left => turn right
            cv2.circle(frame, (50,50), 5, (0, 255, 0), -1, 4)
        elif xx > (2*rows/3) :    #Head on right => turn left
            cv2.circle(frame, (50,50), 5, (255, 0, 0), -1, 4)
        else :                    #Head on middle => don't do anything
            cv2.circle(frame, (50,50), 5, (0, 0, 255), -1, 4)
	

        #print(compt)
    #We draw a contours with the points we have detected
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    ########################################################################################################

    
    final_frame = cv2.hconcat((opening, mask))

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(final_frame,"contours : " + str(len(contours)),(10,50), font, 1,(255,255,255),1,cv2.LINE_AA)

    fin = time.time()
    timeMoy.append(fin-debut)

    # Display the result
    cv2.imshow('image',frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

Meantime = sum(timeMoy) / len(timeMoy)
print(Meantime)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
