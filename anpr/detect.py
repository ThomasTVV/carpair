import os
from os import listdir
from os.path import isfile, join
import re
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from core.functions import *
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

#Path for images + names of images to run on.
mypath = "./data/images"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
stringoffiles = ', '.join(str( mypath + "/" + x) for x in onlyfiles)

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_list('images', stringoffiles, 'path to input image')
flags.DEFINE_string('output', './detections/', 'path to output folder')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('count', False, 'count objects within images')
flags.DEFINE_boolean('dont_show', False, 'dont show image output')
flags.DEFINE_boolean('info', False, 'print info on detections')
flags.DEFINE_boolean('crop', False, 'crop detections from images')
flags.DEFINE_boolean('ocr', False, 'perform generic OCR on detection regions')
flags.DEFINE_boolean('plate', False, 'perform license plate recognition')

def main(_argv):
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    images = FLAGS.images

    #dict for carID and numberplates 
    plateReadings = {}

    #Load model
    saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])

    # loop through images in list and run Yolov4 model on each
    for count, image_path in enumerate(images, 1):
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.
        
        # get image name by using split method
        image_name = image_path.split('/')[-1]
        image_name = image_name.split('.')[0]

        #CarId for later refference in DB
        carID = image_name.split('-')[0]

        #Add key to dictionary if not added
        if carID not in plateReadings:
            plateReadings[carID] = []

        images_data = []
        for i in range(1):
            images_data.append(image_data)
        images_data = np.asarray(images_data).astype(np.float32)

        infer = saved_model_loaded.signatures['serving_default']
        batch_data = tf.constant(images_data)
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]

        # run non max suppression on detections
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = original_image.shape
        bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)
        
        # hold all detection data in one variable
        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        allowed_classes = list(class_names.values())

        #Preprocessing and OCR in utils.py
        try:
            result = utils.draw_bbox(original_image, pred_bbox, FLAGS.info, allowed_classes=allowed_classes, read_plate = FLAGS.plate)
            image = result[0] #still here if we want to show each detection as pop.up (look at old code to suceessfully integrate)
            numberplate = result[1]

            # Only append if string isn't empty
            if numberplate:
                plateReadings[carID].append(numberplate)

            print(plateReadings)

        except:
            print("Something went wrong w." + image_name)

    #Logic for validating carplates
    validatedCarPlates = {}

    #Two leading letters in capital + 5 numbers
    regexVal = re.compile("[A-Z]{2}[0-9]{5}")

    for carID, plateList in plateReadings.items():
        for plate in plateList:
            #Check min. length and if regex match is present
            if len(plate) >= 7 and regexVal.search(plate): 
                #Store only the regex match and ignore leading and following charchters
                result = regexVal.search(plate).group(0)
                #Only add the first elemnent that matches the criteria (first pics in listing often has better view)
                if carID not in validatedCarPlates: 
                    validatedCarPlates[carID] = result

    #Print sucesfully identified numberplates <-- needs to be inserted into sql                
    print(validatedCarPlates)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
