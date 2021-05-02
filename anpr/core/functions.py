import os
from cv2 import cv2
import random
import numpy as np
import tensorflow as tf
import pytesseract
from core.utils import read_class_names
from core.config import cfg

        
# function to run general Tesseract OCR on any detections (default one saved for comparison)
# def ocr(img, data):
#     boxes, scores, classes, num_objects = data
#     class_names = read_class_names(cfg.YOLO.CLASSES)
#     for i in range(num_objects):
#         # get class name for detection
#         class_index = int(classes[i])
#         class_name = class_names[class_index]
#         # separate coordinates from box
#         xmin, ymin, xmax, ymax = boxes[i]
#         # get the subimage that makes up the bounded region and take an additional 5 pixels on each side
#         box = img[int(ymin)-5:int(ymax)+5, int(xmin)-5:int(xmax)+5]
#         # grayscale region within bounding box
#         gray = cv2.cvtColor(box, cv2.COLOR_RGB2GRAY)
#         # threshold the image using Otsus method to preprocess for tesseract
#         thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#         # perform a median blur to smooth image slightly
#         blur = cv2.medianBlur(thresh, 3)
#         # resize image to double the original size as tesseract does better with certain text size
#         blur = cv2.resize(blur, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
#         # run tesseract and convert image text to string
#         try:
#             text = pytesseract.image_to_string(blur, config='--psm 11 --oem 3')
#             print("Class: {}, Text Extracted: {}".format(class_name, text))
#         except: 
#             text = None