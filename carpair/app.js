const express = require('express');
const app = express();
const router = express.Router();

const path = __dirname + '/views/';
const port = 8080;

var mysql = require('mysql');

// Template engine
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

// Specify static root directory
app.use(express.static(path));

// Mount router as middleware: 
app.use('/', router); 

// Print message in console at bootup
app.listen(port, function () {
    console.log(`I\'m listening for you on port ${port}!`)
});

// Print request method in the console
router.use(function (req,res,next) {
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
    var query = `SELECT * FROM scrapedCars INNER JOIN carData ON scrapedCars.numberplate = carData.numberplate;`;

    handleSql(query, "return lots", function (result) {
        res.send(result);
    });
});