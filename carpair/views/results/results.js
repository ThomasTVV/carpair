var resultp = document.getElementById("resultp");

function testApiRequest(par1, par2) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            //var lot = this.responseText; //bruges til tekst
            //var result = JSON.parse(this.response); //bruges til json
            //ShelfCount = result[0].count;
            //TrayCount = result[1].count;
            //ProduceCount = result[2].count;
            //LotCount = result[3].count;
        }
    };
    xmlhttp.open("GET", `newTest?parameter1=${par1}&parameter2=${par2}`, true);
    xmlhttp.send();
}


function loadCars() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.response);
            console.log(result);

            for (var i = 0; i < 2; i++) {
                resultp.innerHTML += `<br>Pris: ${result[i]["price"]}, Nummerplade: ${result[i]["numberplate"]} osv... (se console for flere mulige elementer)`;
            }
        }
    };
    xmlhttp.open("GET", `getCars`, true);
    xmlhttp.send();
}

loadCars();
