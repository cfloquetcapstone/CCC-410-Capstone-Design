
### Charlie Floquet Capstone Project
# Organization Script


### Requisites:
#  - For now, a large folder (OriginalImages) of redundant folders of same id photos with different colors
#  - EX: 3001black, 3001blue, 3004yellow,3004red, etc.
#

## Add any colors that are used within "OriginalImages"

currentColors = ["black","white","bgray","dgray"]


######### IMPORTS ##########

## for accessing the file directory structure of the host OS
import os 
print("Imported Local File System Successfully.")

# import OrderedDict to remove duplicates from ID list
from collections import OrderedDict
print("Imported OrderedDict Successfully.")

# import RE to discern between ID and color in foldername
import re
print("Imported RE Successfully.")

# import copy_tree to copy folder contents
from distutils.dir_util import copy_tree
print("Imported copy_tree Successfully.")

#lets define the original images directory
partList = os.listdir('/home/cfloquet/Pictures/OriginalImages/')
#print(partList)

############### Obtain Working Directory ################

# we can use the imported OS command to find what the relative file path should be, sort of. 
path = os.getcwd()
print(path)

try:
    # Lets try to make the folder to store our newly organized images. 
    os.mkdir(path+"/Pictures/GroupedImages")
except:
    pass

#We will use this to store the IDs of the pieces in OriginalImages
IDList = []

#print a list of the images found within our target dataset folder
for part in partList:
    #split the name of the folder between the ID and the color
    match = re.match(r"([0-9]+)([a-z]+)", part, re.I)
    if match:
        # match.groups(1) = the color of the brick
        # match.groups(0) = the ID of the brick
        #items = match.groups()
        ID = match.group(1)
        #add the ID to a list we've already defined above. 
        IDList.append(ID)

# Use OrderedDict to remove any repeating IDs
IDList = list(OrderedDict.fromkeys(IDList))
#print(IDList)

#iterate through the list of IDs imported from the folder 
for id in IDList:
    #also iterate through the colors we defined above!
    for color in currentColors:
        #define the folder we will be copying from
        fromFolder = (path+"/Pictures/OriginalImages/"+id+color)
        # define the folder we are copying the images to
        toFolder = (path+"/Pictures/GroupedImages/"+id)
        # some folders dont have all the colors, so to avoid errors lets use try/except loops
        try:
            # first we need to try to make the path for the piece 
            os.mkdir(path+"/Pictures/GroupedImages/"+id)
        except:
            pass
        try:
            #now we can use the copy_tree function to copy everything from the defined filepaths
            copy_tree(fromFolder, toFolder)
        except:
            # We will print when we are missing certain colors, which is a lot. 
            print("Couldn't find "+id+" in "+color+". Skipping.")

#print(partList)