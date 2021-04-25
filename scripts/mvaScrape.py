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


    def openPage(self, url, numberplate):
        self.driver.get(url)
        self.driver.find_element_by_id("regnr").click()
        self.driver.find_element_by_id("soegeord").send_keys(numberplate)
        currentUrl = self.driver.current_url
        self.driver.find_element_by_id("fremsoegKtBtn").click()

        self.waitForPageLoad(currentUrl)
        self.scanPage(numberplate)

    def scanPage(self, numberplate):
        results = {}
        results["title"] = self.getValue("Mærke, Model, Variant:")
        results["value"] = self.getValue("Første registrerings­dato:")
        #TODO: FIND ALLE VALUES!!! KRÆVER AT MAN SKIFTER LIDT SIDE.
        print(results)

    def waitForPageLoad(self, currentUrl):
        for i in range(120):
            sleep(1)
            if currentUrl != self.driver.current_url:
                return
        print("Den er ikke loadetttt!!!!")

    def getValue(self, spanKey):
        key = self.driver.find_element_by_xpath("//span[.='"+spanKey+"']")
        parent = key.find_element_by_xpath("./..")
        return parent.find_elements_by_css_selector("span.value")[0].text


if __name__ == '__main__':
    temp = ImportBot()
    temp.openPage("https://motorregister.skat.dk/dmr-kerne/dk/skat/dmr/front/portlets/koeretoejdetaljer/visKoeretoej/VisKoeretoejController.jpf", "cs69956")

