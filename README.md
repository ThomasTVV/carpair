# carpair
Compare car


## YoloV4 setup.

**Install dependencies set as requirements**

```c
# TensorFlow CPU
pip install -r requirements.txt

# TensorFlow GPU
pip install -r requirements-gpu.txt
```

**Download pre-trained license plate weights**

[https://drive.google.com/file/d/1EUPtbtdF0bjRtNjGv436vDY28EN5DXDH/view](https://drive.google.com/file/d/1EUPtbtdF0bjRtNjGv436vDY28EN5DXDH/view)

Copy and paste your custom .weights file into the 'data' folder and copy and paste your custom .names into the 'data/classes/' folder.

on line 14 of 'core/config.py' file. Update the code to point at your custom .names file as seen below.


![editcode](https://raw.githubusercontent.com/theAIGuysCode/yolov4-custom-functions/master/data/helpers/custom_config.png)


## Creating and running the model

convert the custom yolov4-weights into the corresponding TensorFlow model files and then run the model.

```c
python save_model.py --weights ./data/custom.weights --output ./checkpoints/custom-416 --input_size 416 --model yolov4 
```

Run the custom yolov4 tensorflow model

```c
# Run custom yolov4 tensorflow model
python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images ./data/images/car1.jpg
```

## Image pre-processing

The function that is in charge of doing the preprocessing and text extraction is called recognize_plate and can be found in the file core/utils.py.

## Setting up Tesseract OCR

In order to run tesseract OCR you must first download the binary files and set them up on your local machine. Please do so before proceeding or commands will not run as expected!

Official Tesseract OCR Github Repo: [tesseract-ocr/tessdoc](https://github.com/tesseract-ocr/tessdoc)

Article for How To Install Tesseract on Mac or Linux Machines: [https://www.pyimagesearch.com/2017/07/03/installing-tesseract-for-ocr/](https://www.pyimagesearch.com/2017/07/03/installing-tesseract-for-ocr/)

For Windows 

[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Running the license place recognition

```c
# Run License Plate Recognition on single image
python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images ./data/images/car2.jpg --plate

# Run License Plate Recognition on multiple images
python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images "./data/images/car5.jpg, ./data/images/car6.jpg"
```

The output from the above command should print any license plate numbers found to your command terminal as well as output and save the following image to the detections folder.

You should be able to see the license plate number printed on the screen above the bounding box found by YOLOv4.
