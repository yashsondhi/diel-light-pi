"""Make images a movie
adapded from https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
Please install opencv as a dependency to run
Requires open cv as a dependedncy
"""

import cv2
import numpy as np
import glob
import os
from tkinter import Tcl
img_array = []
path=input("choose path:")
count=0

file_limit=10000 # cahnge file limit if you want many files, but takes longer

for filename in sorted(glob.glob(path+"/*.jpg"),key =os.path.basename):
    if(count<file_limit):
        count=count+1
        #print(filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    else:
        break    

os.chdir(path+"/")
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
