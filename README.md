# CarPair
CarPair seeks to establish trust and streamline the car sales process, by establishing a decentralized platform that makes use of a webscraper that scours the web for car listings. The gathered data is then further complimented by using Automatic Numberplate Recognition(ANPR) software to extract number plates from car listings, which further enriches the gathered data, by using external API's. This results in a decentralized platform with car listings that have universally enriched data, whose parameters can then be further searched and filtered through.


# Run the application

## NPM

- Make sure to install NPM and Node on your machine.
- Clone the repository and CD into the folder \carpair\carpair.
- Run `npm install` to install dependencies.
- To start the application, run `node app.js` in the folder.
- Visit http://localhost:8080




# Administrating the back-end
Please make sure that you have the correct libraries installed in order for the application to properly function.

## Scrape Car-listings from dba.dk
go to carpair/scripts and open the command prompt and run
```c
python dba.py
```




## Populating your machine with images to run ANPR on

go to carpair/scripts/imgscraper.py and change the path in the method DownloadImgFromUrl(), so that it points to the carpair/anpr/Plate_examples folder in the carpair directory.

`save_path = 'C:/Users/user/Desktop/carpair/anpr/data/images`

run the imgscraper.py script located in carpair/scripts to get all images to run anpr on

```c
python imgscraper.py
```




## Running the license place recognition on the gathered images

Run the following command in the carpair/anpr folder to run the ANPR which ultimately outputs the correctly identified numberplates to the database

```c
python anpr.py
```



## Scrape MVA to get data corresponding to the numberplate gathered from the ANPR

Run the following script with the commandopromot in carpair/scripts

```c
python mvaScrape.py
```

Your application should now contain the cars, where a number plate has correctly been identified, with additional data, than its original listing had.

_
At the given time the ANPR does not insert number plates into the DB, for lack of interference when presenting the application_

