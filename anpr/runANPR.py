import os
from os import listdir
from os.path import isfile, join
mypath = "./data/images"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
stringoffiles = ', '.join(str( mypath + "/" + x) for x in onlyfiles)
commandstring = "python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images \""+ stringoffiles + "\" --plate"
os.system(commandstring)
