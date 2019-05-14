#!/usr/bin/env python

import serial
import time

p = 100 # angle pan initial
t = 60 # angle tilt initial

# Bornes pan :
pMin = 80
pMax = 120

# Bornes tilt :
tMin = 40
tMax = 80


# Ouverture de la liaison serie :
ser=serial.Serial('/dev/ttyACM0', 115200, timeout = 0.02, writeTimeout=0.02)
time.sleep(0.5)
ready = True
		

# Oriente les yeux avec des angles p et t:
def regarde(p,t) :
	txt = "{:03d}".format(int(p)) + "{:03d}".format(int(t))*3 + "\n"
	print(txt)
	ser.write(txt.encode())
	ready = False
	
# envoie les consignes a l'arduino s'il est pret :
def update():
	global p
	global t
	global ready
	
	if(ser.in_waiting) :
		etat = ser.readline().decode()
		if(len(etat)>0) :
			if(etat[0]=='r') :
				r = (int(float(etat[1:-1])))
				if(not ready and r) :
					print("Mouvement termine ("+str(p)+","+str(t)+")")
				ready = r
			if(etat[0]=='t') :
				t = (int(float(etat[1:-1])))
			if(etat[0]=='p') :
				p = (int(float(etat[1:-1])))
				
				
def isReady() :
	return ready
