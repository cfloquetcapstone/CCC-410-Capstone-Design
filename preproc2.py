## Charlie FLoquet
## CCC-ITS-410: LEGOMLID Preprocessing Program
## 10/19/20

## PRE REQUISITE FOLDERS: 
# - "OriginalImages" Folder, with subfolders of bricks with associated names
# - "ProcessedImages" Folder needs to be created in the same folder as "OriginalImages"

## Image Pre-Processing Script

#Import Matplot Libraries for Axes3D module which we will use for plotting points
from mpl_toolkits.mplot3d import Axes3D
print("Imported Axes3D Successfully.")

#Import scikit-learn libraries which includes StandardScaler requisite for ML
from sklearn.preprocessing import StandardScaler
print("Imported StandardScaler Successfully.")

#Import pyplot as 'plt' for later use
import matplotlib.pyplot as plt
print("Imported MatPlotLib Successfully.")

#We will need to import numpy for some linear algebra
import numpy as np 
print("Imported Numpy Successfully.")

## for accessing the file directory structure of the host OS
import os 
print("Imported Local File System Successfully.")

# We will need to import pandas as well for data processing, and CSV file I/O
import pandas as pd
print("Imported Pandas Successfully.")

#Finally, using pickle we will want to save the data so that we don't have to generate it from scratch every time we do this. 
import pickle
print("Imported Pickle Successfully.")

## we need to install and import opencv so that we can open and read image files
import cv2
print("Imported OpenCV Successfully.")

# TQDM I've heard is a handy progress bar library, and since we will be doing beefy stuff in this project I would like a progress bar. 
from tqdm import tqdm
print("Imported TQDM Successfully.")

# import Pathlib to view stored image files for preproc and training
import pathlib
print("All prerequisites passed, good to proceed!")


### Importing Raw Image Files ###

#testing pathlib module
folderPath = pathlib.Path('/home/cfloquet/Documents/Capstone/LEGOMLIDWorking/LEGOMLID-3-3-21/OriginalImages/')
print(folderPath)

#print a list of the images found within our target dataset folder
for imgLoc in folderPath.iterdir():
	print(imgLoc)

#import random to randomly shuffle images within array to stimulate different neural paths. 

### Catagorize the Images into a Static List ###
brickTypes = sorted(imgLoc.name for imgLoc in folderPath.glob('*/') if imgLoc.is_dir())

## Retrieve the total count of brick types we have in the folder
brickTypeCount = len(brickTypes)

#define the folder path to save image to
try:
    os.mkdir("../ProcessedImages")
except:
    pass
#--->I want to have a list of the different types of bricks that will identified, which will be taken directly from the files found within 'cropped_training_images'
print("Number of Brick Types In Folder: ",brickTypeCount)
print("Current Inventory: ",brickTypes)

### Resize Training Images, Converting to Grayscale ###

#define array to store finalized training image data in
dataForTraining = []
def developTrainingData():
    # iterate through the different types of pieces (folders)
    for piece in brickTypes:
        #define path to training images
        imgLoc = os.path.join(folderPath,piece) 
	# now we need to retrieve the classification of piece associated
        classification = brickTypes.index(piece)
        #define the unique file structure for the specific piece
        pieceFilePath = "/home/cfloquet/Documents/Capstone/LEGOMLIDWorking/LEGOMLID-3-3-21/ProcessedImages/"+piece
        #define the folder path to save image to
        try:
            os.mkdir(pieceFilePath)
        except:
            pass
        print("Created ",pieceFilePath)
        print("Processing Images for: ",piece)
        #go through each catagory and resize and recolor each image, before adding it to dataForTraining array
        for picture in tqdm(os.listdir(imgLoc)): 
                #load the exmample.  It is a white piece, the most difficult to detect!
                img_example=cv2.imread(os.path.join(imgLoc,picture))
                img_gray=cv2.cvtColor(img_example, cv2.COLOR_BGR2GRAY)

                #load a background, so we can extract it and make it easy to detect the object.
                img_bg=cv2.imread("/home/cfloquet/Documents/Capstone/LEGOMLIDWorking/LEGOMLID-3-3-21/bg.jpg")
                img_bg_gray=cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)

                #calculate the difference between background and foreground
                diff_gray=cv2.absdiff(img_bg_gray,img_gray)
                # We are adding gausian blur for smoothness
                diff_gray_blur = cv2.GaussianBlur(diff_gray,(5,5),0)

                ret, img_tresh = cv2.threshold(diff_gray_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                arr_cnt, a2 = cv2.findContours(img_tresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                cv2.imwrite("GrayDifference.jpg",diff_gray_blur)

                img_example=cv2.imread("GrayDifference.jpg")

                # get the dimensions of the image
                height, width, channels = img_example.shape

                # shorten the variable names
                w=width
                h=height

                validcontours=[]
                contour_index=-1

                # iterate through each contour found
                for i in arr_cnt:

                    contour_index=contour_index+1
                    ca=cv2.contourArea(i)

                    # Calculate W/H Ratio of image
                    x,y,w,h = cv2.boundingRect(i)
                    aspect_ratio = float(w)/h

                    # Flag as edge_noise if the object is at a Corner
                    # Contours at the edges of the image are most likely not valid contours
                    edge_noise=False
                    # if contour starts at x=0 then it's on th edge
                    if x==0:
                        edge_noise=True
                    if y==0:
                        edge_noise=True
                    # if the contour x value + its contour width exceeds image width, it is on an edge
                    if (x+w)==width:
                        edge_noise=True
                    if (y+h)==height:
                        edge_noise=True
                            
                    # DISCARD noise with measure by area (1x1 round plate dimensions is 1300)
                    # if by any chance a contour is drawn on one pixel, this catches it.
                    if ca>1300:

                        # DISCARD as noise if W/H ratio > 7 to 1 (1x6 plate is 700px to 100px)
                        # the conveyor belt has a join line that sometimes is detected as a contour, this ignores it based on w/h ratio
                        if aspect_ratio<=6:
                            
                            # DISCARD if at the Edge
                            if edge_noise==False:
                                validcontours.append(contour_index)

                # copy the original picture
                img_withcontours=img_example.copy()
                                
                # call out if more than 1 valid contour is found
                if len(validcontours)>1:
                    print("There is more than 1 object in the picture")
                else:
                    if len(validcontours)==1:
                        print("One object detected")
                    else:
                        print("No objects detected")
                        # FYI: code below will most likely error out as it tries to iterate on an array
                    
                # it might be possible we have more than 1 validcontour, iterating through them here
                # if there is zero contours, this most likely will error out
                img_withrectangle=img_example.copy()
                for i in validcontours:
                    x,y,w,h = cv2.boundingRect(arr_cnt[i])
                    cv2.rectangle(img_withrectangle,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)
                    print (x,y,w,h)
                    cropped = img_withrectangle[y-5:y+h+5,x-5:x+w+5]

                #define the more specific ID file path
                idFilePath = os.path.join(pieceFilePath, str(picture))
                #export as JPG image to the correct file path
                cv2.imwrite(idFilePath, cropped)
                
 
#call training data function
developTrainingData()

print("Images Resized, Recolored, and External Save Successful.")
#show length of dataForTraining array







