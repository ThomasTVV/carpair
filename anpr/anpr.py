# remove warning message
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# required library
import cv2
import numpy as np
from local_utils import detect_lp
from os.path import splitext,basename
from keras.models import model_from_json
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
from sklearn.preprocessing import LabelEncoder
import glob
import re

def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        print("Loading model successfully...")
        return model
    except Exception as e:
        print(e)

def preprocess_image(image_path,resize=False):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img

def get_plate(image_path, Dmax=608, Dmin = 608):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    return vehicle, LpImg, cor

#Processing
def sort_contours(cnts,reverse = False):
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts

# pre-processing input images and pedict with model
def predict_from_model(image,model,labels):
    image = cv2.resize(image,(80,80))
    image = np.stack((image,)*3, axis=-1)
    prediction = labels.inverse_transform([np.argmax(model.predict(image[np.newaxis,:]))])
    return prediction


# Load License plate detection model
wpod_net_path = "wpod-net.json"
wpod_net = load_model(wpod_net_path)

# Load model architecture, weight and labels for characters
json_file = open('MobileNets_character_recognition.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("License_character_recognition_weight.h5")
print("[INFO] Model loaded successfully...")

labels = LabelEncoder()
labels.classes_ = np.load('license_character_classes.npy')
print("[INFO] Labels loaded successfully...")

#dict for carID and numberplates 
plateReadings = {}

# Create a list of image paths 
image_paths = glob.glob("Plate_examples/*.jpg")

#Apply operations to all images in folder
for test_image_path in image_paths:
    try:

         # get image name by using split method
        image_name = test_image_path.split('/')[-1]
        image_name = test_image_path.split('.')[0]

        #CarId for later refference in DB
        carID = test_image_path.split('-')[0]

        #Add key to dictionary if not added
        if carID not in plateReadings:
            plateReadings[carID] = []

        #Detect license plate (WPOD-NET)
        vehicle, LpImg,cor = get_plate(test_image_path)

        #check if there is at least one license image
        if (len(LpImg)): 
            # Scales, calculates absolute values, and converts the result to 8-bit.
            plate_image = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
            # convert to grayscale and blur the image
            gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(7,7),0)
            # Applied inversed thresh_binary 
            binary = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)

        #Identify contours
        cont, _  = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # creat a copy version "test_roi" of plat_image to draw bounding box
        test_roi = plate_image.copy()

        # Initialize a list which will be used to append charater images
        crop_characters = []

        # define standard width and height of character
        digit_w, digit_h = 30, 60

        for c in sort_contours(cont):
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = h/w
            # Only select contour with defined ratio
            if 1<=ratio<=3.5: 
                # Select contour which has the height larger than 50% of the plate
                if h/plate_image.shape[0]>=0.5: 

                    # Draw bounding box arroung digit number
                    cv2.rectangle(test_roi, (x, y), (x + w, y + h), (0, 255,0), 2)

                    # Sperate number and give prediction
                    curr_num = thre_mor[y:y+h,x:x+w]
                    curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
                    _, curr_num = cv2.threshold(curr_num, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    crop_characters.append(curr_num)

        print("Detect {} letters...".format(len(crop_characters)))
        final_string = ''

        for i,character in enumerate(crop_characters):
            title = np.array2string(predict_from_model(character,model,labels))
            final_string+=title.strip("'[]")
        print(final_string)

        # Only append if string isn't empty
        if final_string:
            plateReadings[carID].append(final_string)
    except:
        print("Exited while using image")

#Dictionary to hold validated carplates
validatedCarPlates = {}

#Two leading letters in capital + 5 numbers
regexVal = re.compile("[A-Z]{2}[0-9]{5}")

#Iterate over all carIDS and all predictions made for each image
for carID, plateList in plateReadings.items():
    for plate in plateList:
        #Check min. length and if regex match is present
        if regexVal.search(plate): 
            #Store only the regex match and ignore leading and following charchters
            result = regexVal.search(plate).group(0)
            #Only add the first elemnent that matches the criteria (first pics in listing often has better view)
            if carID not in validatedCarPlates: 
                validatedCarPlates[carID] = result

#Print sucesfully identified numberplates              
print(validatedCarPlates)



