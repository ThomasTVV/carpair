# CarPair
CarPair seeks to establish trust and streamline the car sales process, by establishing a decentralized platform that makes use of a webscraper that scours the web for car listings. The gathered data is then further complimented by using Automatic Numberplate Recognition(ANPR) software to extract number plates from car listings, which further enriches the gathered data, by using external API's. This results in a decentralized platform with car listings that have universally enriched data, whose parameters can then be further searched and filtered through.


# Run the application

## NPM

- Make sure to install NPM and Node on your machine.
- Clone the repository and CD into the folder \carpair\carpair.
- Run `npm install` to install dependencies.
- To start the application, run `node app.js` in the folder.
- Visit http://localhost:8080



## Running the license place recognition

Run the following command in the anpr folder to run the ANPR which ultimately outputs the correctly identified numberplates to the database, proccessed on images placed in carpair/anpr/

```c
python anpr.py
```
