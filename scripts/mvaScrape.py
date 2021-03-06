from selenium import webdriver
from time import sleep
import mysql.connector

class ImportBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        #self.driver.maximize_window()
        self.mydb = mysql.connector.connect(
                host="mysql112.unoeuro.com",
                user="sikkermail_konsulent_dk",
                password="zrdEhaktw2g9",
                database="sikkermail_konsulent_dk_db"
            )

    def loadNew(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT carData.numberplate, price from carData INNER JOIN scrapedCars ON carData.numberplate = scrapedCars.numberplate WHERE title is null;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        for result in myresult:
            self.openPage("https://motorregister.skat.dk/dmr-kerne/dk/skat/dmr/front/portlets/koeretoejdetaljer/visKoeretoej/VisKoeretoejController.jpf", result[0], result[1])

    def openPage(self, url, numberplate, price):
        self.driver.get(url)
        self.driver.find_element_by_id("regnr").click()
        self.driver.find_element_by_id("soegeord").send_keys(numberplate)
        currentUrl = self.driver.current_url
        self.driver.find_element_by_id("fremsoegKtBtn").click()

        self.waitForPageLoad(currentUrl)
        results = self.scanPage(price)
        self.updateDB(numberplate, results)

    def getIndex(self, results, price):
        kml = float(results["kml"].replace(",", "."))
        fuelCost = round(16000 / kml * 10)

        km = int(results["kilometer"])
        kmCost = 0

        if km <= 60: # source: https://santanderconsumer.dk/magasinet/bil-og-mc/hvad-koster-det-at-vedligeholde-en-bil/
            kmCost = 3500
        elif km <= 120:
            kmCost = 11000
        else:
            kmCost = 12000

        taxCost = int(results["weighttax"]) * 2
        yearlyCost = fuelCost + taxCost + kmCost

        age = 2021 - int(results["manufactured"])

        score = self.calculateScore(price, age, yearlyCost)
        return score

    def scanPage(self, price):
        results = {}
        results["title"] = self.getValue("M??rke, Model, Variant:")
        tmp = results["title"].split(", ")
        results["brand"] = tmp[0]
        results["model"] = tmp[1]

        tmp = self.getValue("F??rste registrerings??dato:")
        results["manufactured"] = tmp.split("-")[2]

        results["kilometer"] = self.getValue2("Kilometerstand:", True)

        self.changePage('//*[@id="li-visKTTabset-1"]/div/a')

        results["fuel"] = self.getValue2("Drivkraft:")
        results["kml"] = self.getValue2("Br??ndstofforbrug:")

        self.changePage('// *[ @ id = "li-visKTTabset-2"] / div / a')

        try:
            results["checkupdate"] = self.getValue2("Beregnet dato for n??ste indkaldelse til periodisk syn:")
        except:
            print("Den er ikke indkaldt til syn.")

        self.changePage('// *[ @ id = "li-visKTTabset-4"] / div / a')

        tmp = self.driver.find_elements_by_css_selector(".stripes-even td:nth-child(7) a span")[0].text
        results["weighttax"] = self.formatWeightTax(tmp)
        results["score"] = self.getIndex(results, price)
        print(results)
        return results

    def waitForPageLoad(self, currentUrl):
        for i in range(120):
            sleep(1)
            if currentUrl != self.driver.current_url:
                return
        print("Den er ikke loadetttt!!!!")

    def changePage(self, buttonxpath):
        currentUrl = self.driver.current_url
        self.driver.find_element_by_xpath(buttonxpath).click()
        self.waitForPageLoad(currentUrl)

    def getValue(self, spanKey):
        key = self.driver.find_element_by_xpath("//span[.='"+spanKey+"']")
        parent = key.find_element_by_xpath("./..")
        return parent.find_elements_by_css_selector("span.value")[0].text

    def getValue2(self, spanKey, multipleResults = False):
        if multipleResults:
            key = self.driver.find_elements_by_xpath("//label[.='"+spanKey+"']")[1]
        else:
            key = self.driver.find_element_by_xpath("//label[.='"+spanKey+"']")

        parent = key.find_element_by_xpath("./..")
        grandparent = parent.find_element_by_xpath("./..")
        value = grandparent.find_element_by_css_selector('div:last-child span').text
        return value

    def formatWeightTax(self, str):
        new = str.split(",")[0]
        new = new.replace(".","")
        return new

    def updateDB(self, numberplate, results):
        mycursor = self.mydb.cursor()
        sql = "UPDATE carData set"
        for key in results:
            sql += f" {key} = '{results[key]}', "

        print(sql)
        sql = sql[:-2]
        sql += f" where numberplate = '{numberplate}';"
        print(sql)
        mycursor.execute(sql)
        self.mydb.commit()

    def calculateScore(self, price, age, yearlyCost):
        averageCost = 24000
        yearlyCostIndex = yearlyCost/averageCost*100

        formulaAge = 480.37*price**-0.357 #from excel, 480,37*price^-0,357
        ageIndex = age/formulaAge*100

        averageIndex = (yearlyCostIndex + ageIndex)/2
        handicap = (price/100000)/5 #dividing by 100.000 to get a small handicap based on the price. And dividing by 5 in order to downscale the handicap. (So price isn't an extremely dominating factor)
        averageIndex = averageIndex * (1 + handicap)
        return round(averageIndex)



if __name__ == '__main__':
    temp = ImportBot()
    #temp.openPage("https://motorregister.skat.dk/dmr-kerne/dk/skat/dmr/front/portlets/koeretoejdetaljer/visKoeretoej/VisKoeretoejController.jpf", "cs69956")
    temp.loadNew()
