# carpair


Install ANPR dependencies by opening your commando prompt and navigating in to the anpr folder and enter the commands shown aswell as installing the necessary files and executables.

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

Copy and paste your custom .weights file into the 'data' folder.


## Creating and running the model

Convert the custom yolov4-weights into the corresponding TensorFlow model files and then run the model.

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

To run tesseract OCR you must first download the binary files and set them up on your local machine.

Windows: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Mac or Linux: [https://www.pyimagesearch.com/2017/07/03/installing-tesseract-for-ocr/](https://www.pyimagesearch.com/2017/07/03/installing-tesseract-for-ocr/)


## Running the license place recognition

```c
# Run License Plate Recognition on single image
python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images ./data/images/car8.jpg --plate

# Run License Plate Recognition on multiple images
python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images "./data/images/car5.jpg, ./data/images/car6.jpg, ./data/images/car7.jpg, ./data/images/car8.jpg, ./data/images/car9.jpg, ./data/images/car10.jpg, ./data/images/car11.jpg, ./data/images/car12.jpg, ./data/images/car13.jpg, ./data/images/car14.jpg, ./data/images/car15.jpg, ./data/images/car16.jpg, ./data/images/car17.jpg, ./data/images/car18.jpg, ./data/images/car19.jpg" --plate"
```


The output from the above command should print any license plate numbers found to your command terminal as well as output and save the following image to the detections folder.

If you don't get a licence plate as output either try a different picture or restart your commando prompt, to let earlier changes set in.

You should be able to see the license plate number printed on the screen above the bounding box found by YOLOv4.
