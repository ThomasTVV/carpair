# CarPair
CarPair seeks to establish trust and streamline the car sales process, by establishing a decentralized platform that makes use of a webscraper that scours the web for car listings. The gathered data is then further complimented by using Automatic Numberplate Recognition(ANPR) software to extract number plates from car listings, which further enriches the gathered data, by using external API's. This results in a decentralized platform with car listings that have universally enriched data, whose parameters can then be further searched and filtered through.


# Run the application

## NPM

- Make sure to install NPM and Node on your machine.
- Clone the repository and CD into the folder \carpair\carpair.
- Run `npm install` to install dependencies.
- To start the application, run `node app.js` in the folder.
- Visit http://localhost:8080



# Run back-end services


## Populating your machine with images to run ANPR on

go to carpair/scripts/imgscraper.py and change the path in the method DownloadImgFromUrl(), so that it points to the /data/images folder in the carpair directory.
This will get images from the database, to run the ANPR on.

```c 
save_path = 'C:/Users/user/Desktop/carpair/anpr/data/images
```

## YoloV4 setup.

_Install ANPR dependencies by opening your commando prompt and navigating in to the anpr folder and enter the commands shown aswell as installing the necessary files and executables._

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

Convert the custom yolov4-weights into the corresponding TensorFlow model.

```c
python save_model.py --weights ./data/custom.weights --output ./checkpoints/custom-416 --input_size 416 --model yolov4 
```


## Image pre-processing

The methods that is in charge of doing the preprocessing and text extraction can be found in the file core/utils.py.

## Setting up Tesseract OCR

To run tesseract OCR you must first download the binary files and set them up on your local machine.

Windows: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Mac or Linux: [https://www.pyimagesearch.com/2017/07/03/installing-tesseract-for-ocr/](https://www.pyimagesearch.com/2017/07/03/installing-tesseract-for-ocr/)

Then go to line 7 in carpair/anpr/core/utils.py and change the path to the destination of your tesseract installation

## Running the license place recognition

Run the following command in the anpr folder to run the ANPR which ultimately outputs the correctly identified numberplates to the database, proccessed on images placed in ./data/images.

```c
python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --plate
```
