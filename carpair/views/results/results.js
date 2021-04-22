var resultp = document.getElementById("container");

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

			for (var i = 0; i < result.length; i++) {
				var row = createDomRow(result, i);
				resultp.innerHTML += row;
			}
        }
    };
    xmlhttp.open("GET", `getCars`, true);
    xmlhttp.send();
}

loadCars();

function createDomRow(json, i) {
	var bgColor = (i % 2) ? "#ffffff" : "#dedede";
	var row = `<div style="padding: 10px 0px; background-color: ${bgColor}"><div class="row h150">
		<div class="col-sm-3">
			<div class="carImg" style="background-image: url('${json[i]["thumbnail"]}'); ">
			</div>
		</div>
		<div class="col-sm-9 width72">
			<div class="row title">
				<div class="col-sm-8">
					${json[i]["title"]}
				</div>
				<div class="col-sm-4" style="color: #01631b">
					${json[i]["price"]}
				</div>
			</div>
		<div class="row">
			<div class="col-sm-4">
				${json[i]["kilometer"]}.000 km
			</div>
			<div class="col-sm-4">
				${json[i]["manufactured"]}
			</div>
			<div class="col-sm-4">
				${json[i]["listingdate"]}
			</div>
		</div>
		<div class="row">
			<div class="col-sm-4">
				${json[i]["kml"]} km/l
			</div>
			<div class="col-sm-4">
				${json[i]["weighttax"]},- weighttax
			</div>
			<div class="col-sm-4">
				${json[i]["zipcode"]}
			</div>
		</div>
		<div class="row">
			<div class="col-sm-4">
				${json[i]["fuel"]}
			</div>
			<div class="col-sm-4">
				${checkUpTime(json[i]["checkupdate"])} months for checkup
			</div>
			<div class="col-sm-4">
				<a target="_blank" href="${json[i]["link"]}">View on DBA.DK</a>
			</div>
		</div>
		</div>
		
	</div></div>`;

	return row;
}

function monthDiff(d1, d2) {
	var months;
	months = (d2.getFullYear() - d1.getFullYear()) * 12;
	months -= d1.getMonth();
	months += d2.getMonth();
	console.log(months);
	return months <= 0 ? 0 : months;
}

function checkUpTime(str) {
	var split = str.split("-");
	var newStr = split[2] + "-" + split[1] + "-" + split[0];
	console.log("newStr er: " + newStr);
	var date = new Date(newStr);
	var today = new Date();
	console.log(date);
	console.log(today);
	return monthDiff(today, date);
}