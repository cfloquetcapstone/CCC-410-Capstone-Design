## Charlie FLoquet
## CCC-ITS-410: LEGOMLID Preprocessing Program
## 10/19/20
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
imgPath = pathlib.Path('../cropped_training_images')
print(imgPath)

#print a list of different types of bricks within training folder
#for img in imgPath.iterdir():
	#print(img)

### Catagorize the Images into a Static List ###

#--->I want to have a list of the different types of bricks that will identified, which will be taken directly from the files found within 'cropped_training_images'


### Standardize Image Size ###

# I think that any resolution above 100x100 will work, but I want to try to get as much resolution as possible without having adverse affects on speed or processing power. This will require testing. 


### Convert to Grayscale


### Store as an array for future reference










































