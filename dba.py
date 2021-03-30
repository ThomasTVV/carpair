from selenium import webdriver
import pyperclip
import pyautogui
from time import sleep
import mysql.connector


#hvad nu hvis der kommer nye biler mens scanningen er igang? Skal have en måde at være sikker på at tage alle. så det ikke bare er "i".
#TODO: gør så den er fuld screen.

class ImportBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.mydb = mysql.connector.connect(
                host="mysql112.unoeuro.com",
                user="sikkermail_konsulent_dk",
                password="zrdEhaktw2g9",
                database="sikkermail_konsulent_dk_db"
            )
        self.oldCarUrls = self.loadOldCars()


    def loadOldCars(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT link FROM scrapedCars"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        result = {"test1", "test2"} #fortæller python at det er et set - og ikke en dict.

        for row in myresult:
            result.add(row[0])

        print(result)
        return result

    def openPage(self, url):
        self.driver.get(url)
        self.driver.find_element_by_id("onetrust-accept-btn-handler").click()
        sleep(5)
        self.scanResults()


    def scanResults(self):
        linksTmp = self.driver.find_elements_by_css_selector(".expandable-box a.listingLink")

        for i in range(len(linksTmp)):
            links = self.driver.find_elements_by_css_selector(".expandable-box a.listingLink")
            linkUrl = links[i].get_attribute("href")
            if linkUrl in self.oldCarUrls:
                print("DEN ER TAAAGET")
                continue
            self.driver.get(linkUrl)
            price = self.driver.find_elements_by_class_name("price-tag")[0].text

            try:
                imageUrl = self.driver.find_elements_by_class_name("primary-printable")[0].get_attribute(
                    "src")  # husk try catch. ikke alle har billeder.
            except:
                imageUrl = "null"
                print("Intet billede!")
            # TODO: kald metode der finder nummerpladen. (husk at tjekke alle billeder)
            self.importData(price, linkUrl)
            #sleep(5)
            self.driver.back()

        self.goToNextPage()

    def importData(self, price, link):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO scrapedCars (price, link) VALUES (%s, %s)"
        val = (price, link)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    def goToNextPage(self):
        buttons = self.driver.find_elements_by_class_name("a-page-link")
        nextPageAvailable = False

        for button in buttons:
            text = button.get_attribute('innerHTML')
            if "Næste" in text:
                nextPageAvailable = True
                button.click()
                break

        if nextPageAvailable:
            sleep(5)
            self.scanResults()
        else:
            print("tak for i aften")
            self.driver.quit()

if __name__ == '__main__':
    temp = ImportBot()
    #temp.openPage("https://www.dba.dk/biler/biler/?fra=privat")
    temp.openPage("https://www.dba.dk/biler/biler/reg-aalborg/?fra=privat&sort=listingdate-desc")

