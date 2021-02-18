import cv2 #sudo apt-get install python-opencv
import numpy as py
import os
import time
from ctypes import *
# allow use to define how many images they want taken using a simple for loop
count = input("Enter # of Pictures Desired: ")
#define the ID of the brick being imaged, 
ID = raw_input("Enter ID of Brick or Figure: ")
# I will be adding passwordless SSH to this functionality in the future for seamless transition of # photos from the PI to my Ubuntu desktop.
#export = raw_input("Export to desktop [y/n]: ")
for picture in range(0,count):
        print("################Move Brick Now#################")
        #this time.sleep function allows me to move the position of the piece in between shots
        time.sleep(2)
        print("################STOP#######################")
	#load arducam shared object file
	arducam_vcm= CDLL('RaspberryPi/Motorized_Focus_Camera/python/lib/libarducam_vcm.so')
	try:
		import picamera
		from picamera.array import PiRGBArray
	except:
		sys.exit(0)
	def focusing(val):
		arducam_vcm.vcm_write(val)
		#print("focus value: {}".format(val))
	def sobel(img):
		img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
		img_sobel = cv2.Sobel(img_gray,cv2.CV_16U,1,1)
		return cv2.mean(img_sobel)[0]
	def laplacian(img):
		img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
		img_sobel = cv2.Laplacian(img_gray,cv2.CV_16U)
		return cv2.mean(img_sobel)[0]
	def calculation(camera):
		rawCapture = PiRGBArray(camera) 
		camera.capture(rawCapture,format="bgr", use_video_port=True)
		image = rawCapture.array
		rawCapture.truncate(0)
		return laplacian(image)
	if __name__ == "__main__":
	    #vcm init
		arducam_vcm.vcm_init()
	    #open camera
		camera = picamera.PiCamera()
		#open camera preview
		camera.start_preview()
		#set camera resolution to 640x480(Small resolution for faster speeds.)
		camera.resolution = (640, 480)
		time.sleep(0.1)
		camera.shutter_speed=30000
		print("Start focusing")
		max_index = 10
		max_value = 0.0
		last_value = 0.0
		dec_count = 0
		focal_distance = 10
		while True:
		    #Adjust focus
			focusing(focal_distance)
			#Take image and calculate image clarity
			val = calculation(camera)
			#Find the maximum image clarity
			if val > max_value:
				max_index = focal_distance
				max_value = val
			#If the image clarity starts to decrease
			if val < last_value:
				dec_count += 1
			else:
				dec_count = 0
			#Image clarity is reduced by six consecutive frames
			if dec_count > 6:
				break
			last_value = val
			#Increase the focal distance
			focal_distance += 15
			if focal_distance > 1000:
				break
	    #Adjust focus to the best
		focusing(max_index)
		time.sleep(1)
		#set camera resolution to 2592x1944
		camera.resolution = (1920,1080)
		#save image to file.
                picture = str(picture)
                pictureName = ("TrainingImages/"+ID+"/"+picture+".jpg")
                folderPath = ("TrainingImages/"+ID)
                try: 
                    os.mkdir(folderPath)
                except: 
                    pass
                print("Image "+picture+" Successfully Saved to "+"TrainingImages/"+ID)
		camera.capture(pictureName)
		print("max index = %d,max value = %lf" % (max_index,max_value))
		#while True:
		#	time.sleep(1)
		camera.stop_preview()
		camera.close()
                #define the storage folder for the image being captured
                image = ("TrainingImages/"+ID+"/"+picture+".jpg")
                uncropped = cv2.imread(image)
                os.remove(image)
                filename = ("TrainingImages/"+ID+"/"+picture+".jpg")
                #[left, top, right, bottom]
                #cropped = uncropped.crop((200, 50, 200, 400))
                # the below comment shows how opencv inteprets image cropping, as an array
                #[StartPixFromTop:EndPixFromTop,StartPixFromLeft:EndPixFromLeft]
                cropped = uncropped[0:1000,300:1300]
                #save the cropped image using the defined file path and name. 
                cv2.imwrite(filename, cropped)
