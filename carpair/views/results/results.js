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

function getParam(param) {
	var url_string = window.location.href;
	var url = new URL(url_string);
	return url.searchParams.get(param);
}

function changePage(newPage) {
	var url_string = window.location.href;
	var currentPage = getParam("page");
	var newString = `page=${newPage}`;

	if (currentPage != null) {
		var currentString = `page=${currentPage}`;
		url_string = url_string.replace(currentString, newString);
	}
	else {
		//TODO: der kan nok komme en lille bug her når de andre parametre også skal vises i url.
		url_string += "?" + newString;
	}
	window.location.href = url_string;
}

function loadCars(jsonStr) {
	var result = JSON.parse(jsonStr);

			for (var i = 0; i < result.length; i++) {
				var row = createDomRow(result, i);
				resultp.innerHTML += row;
			}
}

function loadCarsCount() {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			var result = JSON.parse(this.response)[0]["count(price)"];
			createPageButtons(result);
		}
	};
	xmlhttp.open("GET", `getCarsCount`, true);
	xmlhttp.send();
}


function createPageButtons(carsCount) {
	var div = document.getElementById("pages");
	var buttons = Math.ceil(carsCount / 3); //OBS!!! 3 fordi vi i testen vil vise 3 biler per side.
	var pagetmp = getParam("page");
	var page = (pagetmp != null) ? pagetmp : 1;

	for (var i = 0; i < buttons; i++) {
		var active = (page - 1 == i) ? "class='active' " : "";
		var button = `<button ${active}onclick='changePage(${i+1})' type='button'>Page ${i+1}</button> `;
		div.innerHTML += button;
	}
}

function createDomRow(json, i) {
	var bgColor = (i % 2) ? "#ffffff" : "#ffffff";
	var row = `<div class="h150container" style="background-color: ${bgColor}"><div class="row h150">
		<div class="col-sm-3" style="height:100%;">
			<div class="carImg" style="background-image: url('${json[i]["thumbnail"]}'); ">
			</div>
		</div>
		<div class="col-sm-9 width72">
			<div class="row title">
				<div class="col-sm-8 singleline">
					${json[i]["title"]}
				</div>
				<div class="col-sm-4" style="color: #01631b">
					${priceFormat(json[i]["price"])}
				</div>
			</div>
		<div class="row details">
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
		<div class="row details">
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
		<div class="row details">
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
	return months <= 0 ? 0 : months;
}

function priceFormat(price) {
	var position = -3;
	var str = price.toString();
	var output = [str.slice(0, position), ".", str.slice(position)].join('');
	output += " kr.";
	return output;
}

function checkUpTime(str) {
	var split = str.split("-");
	var newStr = split[2] + "-" + split[1] + "-" + split[0];
	var date = new Date(newStr);
	var today = new Date();
	return monthDiff(today, date);
}