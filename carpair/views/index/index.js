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



function storeData() {
    var tax = document.getElementById("tax").value;
    var brand = document.getElementById("brand").value;
    var fuel = document.getElementById("fuel").value;
    var KML = document.getElementById("KML").value;
    var price = document.getElementById("price").value;
    var totalKM = document.getElementById("totalKM").value;
    var nextService = document.getElementById("nextService").value;
    var area = document.getElementById("area").value;
    console.log(tax, brand, fuel, KML, price, totalKM, nextService, area);
};


function CreateQuery(){

}





//SQLQUERY = 'SELECT * FROM Cars WHERE BRAND =" ${number}" AND Fuel="${number}"';