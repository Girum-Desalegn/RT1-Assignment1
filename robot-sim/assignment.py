from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for grab the token"""

d_release=0.8
""" float: Threshold for release the token"""

R = Robot()
""" instance of the class Robot"""

mylist=[]
""" list: collect the code of grabbed token"""

base_token=True
""" boolean: to select the code number of the base token"""

base_token_code=0
""" integer: to store the code number of the base token"""

grabbed = True
""" boolean: to operate release and grab the token"""

count = 0
""" integer: to store the number of released token"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token_grab():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	code (integer): the given code number of the token (0 if no token is detected)
    """
    dist=100
    for token in R.see():
    	if token.dist < dist and token.info.code not in mylist : # we have to initialize the base token and the robot will go to grab the token that must be less than dist and the token is not picked and the token is not the base token
        	dist=token.dist
        	rot_y=token.rot_y
        	code=token.info.code
    if dist==100:
    	return -1, -1,0
    else:
   	return dist, rot_y, code
   	
def find_base_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the base token (-1 if no token is detected)
	rot_y (float): angle between the robot and the base token (-1 if no token is detected)
	code (integer): the given code number of the token (0 if no token is detected)
    """
    global base_token, base_token_code
    dist=100
    if base_token == True:
    	for token in R.see():
    		base_token_code=token.info.code
    		base_token = False
    for token in R.see():	    
    	if token.info.code == base_token_code : # when robot will release the token towards base token
		dist=token.dist
		rot_y=token.rot_y
		code=token.info.code   
    if dist==100:
    	return -1, -1,0
    else:
   	return dist, rot_y, code     
      
while 1:
    if grabbed==True:
    	dist, rot_y,code = find_token_grab()
    else:
    	dist, rot_y,code = find_base_token()    
    if dist==-1: # if no token is detected, we make the robot turn 
    	if count==6:   # If the robot release all token in the base token, the robot finish its task.
        	print("THE TASK IS COMPLETED")
        	exit()
	else:
		print("The robot can't detect any token!!")
		turn(10, 0.5)
    elif dist <d_th and grabbed == True: # if the robot close to the token and grappebed is true, it trys to grab the token.
        print("Found it!")
        R.grab() # if the robot grab the token then find the base token and release it. 
        print("Gotcha!")
        turn(10,0.5)
        mylist.append(code)
        grabbed = False   # grabbed is false because after grab it must be release the token at specified place
    elif dist <d_release and grabbed == False: # if the robot reaches at release distance drop the token and then find the other token to take back
        R.release()
        print ("Released successfully")
        count=count+1
        drive(-10,2)
        turn(10,2)
        mylist.append(code)
        grabbed=True     # After relase the grabbed must be True to grap other token
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, It go forward
    	print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, It moves it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.6)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.6)
    
