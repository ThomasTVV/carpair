const express = require('express');
const app = express();
const router = express.Router();
var bodyParser = require('body-parser');

const path = __dirname + '/views/';
const port = 8080;

var mysql = require('mysql');

const carsPerPage = 3;


// Template engine
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

// Used to extract data from the login form
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Specify static root directory
app.use(express.static(path));

// Mount router as middleware: 
app.use('/', router);

// Print message in console at bootup
app.listen(port, function () {
    console.log(`I\'m listening for you on port ${port}!`)
});

// Print request method in the console
router.use(function (req, res, next) {
    console.log('/' + req.method);
    next();
});

// results route
app.get('/results/', function (req, res) {
    res.render(path + 'results/results.html');
});

// Index route
app.get('/', function (req, res) {
    //res.render(path + 'index/index.html', { hej: count[0].count.toString() }); //s�dan sendes variabler videre.
    res.render(path + 'index/index.html');
});

// Handling sql 
function handleSql(query, responseAction = "", callback) {

    var con = mysql.createConnection({
        host: "mysql112.unoeuro.com",
        user: "sikkermail_konsulent_dk",
        password: "zrdEhaktw2g9",
        database: "sikkermail_konsulent_dk_db"
    });
    con.connect(function (err) {
        if (err) throw err;
    });
    con.query(query, function (err, result, fields) {
        if (err) throw err;

        if (responseAction == "return id") {
            return callback(result[0].id);
        }
        else if (responseAction == "return lots") {
            callback(result);
        }

    });
    con.end();
};

//eksempel p� at inds�tte
app.get('/results/newTest', function (req, res) {
    var par1 = req.query.parameter1;
    var par2 = req.query.parameter2;

    var columns = "`shelf`, `tray`";
    var valuesString = `${par1}, ${par2}`;

    var query = `insert into lots (${columns}) values (${valuesString});`;
    handleSql(query);
    res.send("WHEEE (response text)");
});

//eksempel p� get
app.get('/results/getStatus', function (req, res) {
    var tray = req.query.tray;
    var query = `SELECT status FROM lots WHERE tray = ${tray} ORDER BY lot DESC LIMIT 1;`;

    handleSql(query, "return lots", function (result) {
        res.send(result[0].status);
    });
});

app.get('/results/getCars', function (req, res) {
    //TODO: Her skal den hente de forskellige parametre ned. Og s� bruge den i sql querien. fx: var tray = req.query.tray;
    var page = req.query.page;
    console.log(page);
    var offsetStr = "";
    if (!isNaN(page)) {
        var offset = (page - 1) * carsPerPage; //3 fordi vi kun viser 3 biler i starten!!
        offsetStr = ` OFFSET ${offset}`;
    }
    var query = `SELECT * FROM scrapedCars INNER JOIN carData ON scrapedCars.numberplate = carData.numberplate LIMIT ${carsPerPage}${offsetStr};`;
    console.log(query);

    handleSql(query, "return lots", function (result) {
        res.send(result);
    });
});

//næsten samme query som ovenfor.
app.get('/results/getCarsCount', function (req, res) {
    var query = `SELECT count(price) FROM scrapedCars INNER JOIN carData ON scrapedCars.numberplate = carData.numberplate;`;

    handleSql(query, "return lots", function (result) {
        res.send(result);
    });
});


// Display car listings dependendt on user input from form
app.get('/results/getFiltered', function (req, res) {
    
    // Get page and pagination  info
    var page = req.query.page;
    var offsetStr = "";
    if (!isNaN(page)) {
        var offset = (page - 1) * carsPerPage; //3 fordi vi kun viser 3 biler i starten!!
        offsetStr = ` OFFSET ${offset}`;
    }
    //Data from form input
    var carFormInput = {
        weighttax: req.query.weighttax,
        brand: req.query.brand,
        fuel: req.query.fuel,
        kml: req.query.kml,
        kilometer: req.query.kilometer,
        area: req.query.area,
        priceMIN: req.query.priceMIN,
        priceMAX: req.query.priceMAX,
        area: req.query.area,
        nextService: req.body.nextService
    };

    // new dictionary to clean up wrong inputs, such as empty strings an "any" selectable
    var cleanFormData = [];

    // Clean up non-entries and "any"
    for (var key in carFormInput) {
        value = carFormInput[key];
        if (value === "" || value === undefined || value == "any") {
            if (key === "priceMIN") {
                cleanFormData["priceMIN"] = 1;
            } else if (key === "priceMAX") {
                cleanFormData["priceMAX"] = 9000000000000000;
            } else {
                cleanFormData[key] = " LIKE '%'";
            }
        }
        else {
            cleanFormData[key] = "= " + value;
        }
    }

    // Insert cleaned dictionary into master query (could be dynamically generated)
    var query =
        'SELECT * FROM scrapedCars INNER JOIN carData ON scrapedCars.numberplate = carData.numberplate ' +
        'WHERE carData.weighttax' + cleanFormData.weighttax +
        ' AND carData.fuel' + cleanFormData.fuel +
        ' AND carData.kml' + cleanFormData.kml +
        ' AND carData.kilometer' + cleanFormData.kilometer +
        ' AND scrapedCars.price' + " BETWEEN " + cleanFormData.priceMIN + " AND " + cleanFormData.priceMAX +
        ' AND scrapedCars.area' + cleanFormData.area + 
        ' AND carData.checkupdate' + cleanFormData.nextService +
        ' AND carData.brand' + cleanFormData.brand + ` LIMIT ${ carsPerPage }${ offsetStr };`;
     

    console.log(query)
    // Execute query and render the results on the page
    handleSql(query, "return lots", function (result) {
        var string = JSON.stringify(result);
        res.render(path + 'results/results.html', { results: string });
    });
});
