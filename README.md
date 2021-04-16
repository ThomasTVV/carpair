# CarPair
CarPair seeks to establish trust and streamline the car sales process, by establishing a decentralized platform that makes use of a webscraper that scours the web for car listings. The gathered data is then further complimented by using Automatic Numberplate Recognition(ANPR) software to extract number plates from car listings, which further enriches the gathered data, by using external API's. This results in a decentralized platform with car listings that have universally enriched data, whose parameters can then be further searched and filtered through.

_Install ANPR dependencies by opening your commando prompt and navigating in to the anpr folder and enter the commands shown aswell as installing the necessary files and executables._

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
# Run License Plate Recognition on multiple images / entire test-dataset
python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images "./data/images/car (1).jpg, ./data/images/car (2).jpg, ./data/images/car (3).jpg, ./data/images/car (4).jpg, ./data/images/car (5).jpg, ./data/images/car (6).jpg, ./data/images/car (7).jpg, ./data/images/car (8).jpg, ./data/images/car (9).jpg, ./data/images/car (10).jpg, ./data/images/car (11).jpg, ./data/images/car (12).jpg, ./data/images/car (13).jpg, ./data/images/car (14).jpg, ./data/images/car (15).jpg, ./data/images/car (16).jpg, ./data/images/car (17).jpg, ./data/images/car (18).jpg, ./data/images/car (19).jpg, ./data/images/car (20).jpg, ./data/images/car (21).jpg, ./data/images/car (22).jpg, ./data/images/car (23).jpg, ./data/images/car (24).jpg, ./data/images/car (25).jpg, ./data/images/car (26).jpg, ./data/images/car (27).jpg, ./data/images/car (28).jpg, ./data/images/car (29).jpg, ./data/images/car (30).jpg, ./data/images/car (31).jpg, ./data/images/car (32).jpg, ./data/images/car (33).jpg, ./data/images/car (34).jpg, ./data/images/car (35).jpg, ./data/images/car (36).jpg, ./data/images/car (37).jpg, ./data/images/car (38).jpg, ./data/images/car (39).jpg, ./data/images/car (40).jpg, ./data/images/car (41).jpg, ./data/images/car (42).jpg, ./data/images/car (43).jpg, ./data/images/car (44).jpg, ./data/images/car (45).jpg, ./data/images/car (46).jpg, ./data/images/car (47).jpg, ./data/images/car (48).jpg, ./data/images/car (49).jpg, ./data/images/car (50).jpg, ./data/images/car (51).jpg, ./data/images/car (52).jpg, ./data/images/car (53).jpg, ./data/images/car (54).jpg, ./data/images/car (55).jpg, ./data/images/car (56).jpg, ./data/images/car (57).jpg, ./data/images/car (58).jpg, ./data/images/car (59).jpg, ./data/images/car (60).jpg, ./data/images/car (61).jpg, ./data/images/car (62).jpg, ./data/images/car (63).jpg, ./data/images/car (64).jpg, ./data/images/car (65).jpg, ./data/images/car (66).jpg, ./data/images/car (67).jpg, ./data/images/car (68).jpg, ./data/images/car (69).jpg, ./data/images/car (70).jpg, ./data/images/car (71).jpg, ./data/images/car (72).jpg, ./data/images/car (73).jpg, ./data/images/car (74).jpg, ./data/images/car (75).jpg, ./data/images/car (76).jpg, ./data/images/car (77).jpg, ./data/images/car (78).jpg, ./data/images/car (79).jpg, ./data/images/car (80).jpg, ./data/images/car (81).jpg, ./data/images/car (82).jpg, ./data/images/car (83).jpg, ./data/images/car (84).jpg, ./data/images/car (85).jpg, ./data/images/car (86).jpg, ./data/images/car (87).jpg, ./data/images/car (88).jpg, ./data/images/car (89).jpg, ./data/images/car (90).jpg, ./data/images/car (91).jpg, ./data/images/car (92).jpg, ./data/images/car (93).jpg, ./data/images/car (94).jpg, ./data/images/car (95).jpg, ./data/images/car (96).jpg, ./data/images/car (97).jpg, ./data/images/car (98).jpg, ./data/images/car (99).jpg, ./data/images/car (100).jpg" --plate
```


The output from the above command should print any license plate numbers found to your command terminal as well as output and save the following image to the detections folder.

If you don't get a licence plate as output either try a different picture or restart your commando prompt, to let earlier changes set in.

You should be able to see the license plate number printed on the screen above the bounding box found by YOLOv4.
