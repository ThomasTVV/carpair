const express = require('express');
const app = express();
const router = express.Router();
var bodyParser = require('body-parser');

const path = __dirname + '/views/';
const port = 8080;

var mysql = require('mysql');

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
    // var query = `SELECT * FROM scrapedCars INNER JOIN carData ON scrapedCars.numberplate = carData.numberplate;`;

    var query = `SELECT * FROM scrapedCars INNER JOIN carData ON scrapedCars.numberplate = carData.numberplate;`;

    handleSql(query, "return lots", function (result) {
        res.send(result);
    });
});


// Display car listings dependendt on user input from form
app.post('/results/getFiltered', function (req, res) {
    //Data from form input
    var carFormInput = {
        tax: req.body.tax,
        brand: req.body.brand,
        fuel: req.body.fuel,
        KML: req.body.KML,
        priceMIN: req.body.priceMIN,
        priceMAX: req.body.priceMAX,
        totalKM: req.body.totalKM,
        nextService: req.body.nextService,
        area: req.body.area
    };

    // new dictionary to clean up wrong inputs, such as empty strings an "any" selectable
    var cleanFormData = [];

    // Clean up non-entries and "any"
    for (var key in carFormInput) {
        value = carFormInput[key];
        if (value === "") {
            cleanFormData[key] = "1=1";
        } else if (value == "any") {
            cleanFormData[key] = "1=1";
        } else {
            cleanFormData[key] = value;
        }
    }

    // Insert cleaned dictionary into master query (could probably be dynamically generated)
    // TO DO: need to add custom functionality such as "AT LEAST" functionality and range between min and max price++
    // TO DO: database table names need to be correct
    var query = 
    'SELECT * FROM scrapedCars INNER JOIN carData ON scrapedCars.numberplate = carData.numberplate' + 
    ' WHERE carData.tax="' + cleanFormData.tax.value +  '" ' +
    ' AND WHERE carData.brand="' + cleanFormData.brand.value + '" ' +
    ' AND WHERE carData.fuel="' + cleanFormData.fuel.value + '" ' +
    ' AND WHERE carData.KML="' + cleanFormData.KML.value + '" ' +
    ' AND WHERE carData.price="' + cleanFormData.priceMIN.value + '" ' + /// add priceMIN + MAX MAGIC HERE
    ' AND WHERE carData.totalKM="' + cleanFormData.totalKM.value + '" ' +
    ' AND WHERE carData.nextService="' + cleanFormData.nextService.value + '" ' +
    ' AND WHERE carData.area="' + cleanFormData.area.value + '";';
   
    // Execute query and render the results on the page
    handleSql(query, "return lots", function (result) {
        var string = JSON.stringify(result);
        res.render(path + 'results/results.html', { results: string });
    });
});
