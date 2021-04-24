from selenium import webdriver
import pyperclip
import pyautogui
from time import sleep
import mysql.connector
from datetime import datetime, timedelta


#hvad nu hvis der kommer nye biler mens scanningen er igang? Skal have en måde at være sikker på at tage alle. så det ikke bare er "i".

class ImportBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
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
        self.dbResetActive()
        sleep(5)
        self.scanResults()


    def scanResults(self):
        linksTmp = self.driver.find_elements_by_css_selector(".expandable-box a.listingLink")

        for i in range(len(linksTmp)):
            links = self.driver.find_elements_by_css_selector(".expandable-box a.listingLink")
            linkUrl = links[i].get_attribute("href")
            if linkUrl in self.oldCarUrls:
                print("DEN ER TAAAGET")
                self.dbSetActive(linkUrl)
                continue
            self.driver.get(linkUrl)
            self.scanCarPage(linkUrl)
            #sleep(5)
            self.driver.back()

        self.goToNextPage()

    def scanCarPage(self, linkUrl):
        price = self.driver.find_elements_by_class_name("price-tag")[0].text

        try:
            imageUrl = self.driver.find_elements_by_class_name("primary-printable")[0].get_attribute(
                "src")  # husk try catch. ikke alle har billeder.
        except:
            imageUrl = "null"
            print("Intet billede!")

        zipTmp = self.driver.find_elements_by_css_selector(".dba-MuiTypography-body1 span:last-child")[0].text
        zipTmp2 = zipTmp.split(", ")
        zip = int(zipTmp2[-1].split(" ")[0])

        area = ""

        if zip < 4999:
            area = "Sjælland"
        elif zip < 5999:
            area = "Fyn"
        elif zip < 6999:
            area = "Sønderjylland"
        elif zip < 7999:
            area = "midtjylland"
        elif zip < 8999:
            area = "Østjylland"
        elif zip < 10000:
            area = "Nordjylland"

        dateTmp = self.driver.find_elements_by_class_name("heading-small")[0].text
        dateStr = ""

        months = ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"]

        if "i dag" in dateTmp.lower():
            today = datetime.now()
            month = months[today.month - 1]
            dateStr = today.strftime("%d. " + month)

        elif "i går" in dateTmp.lower():
            yesterday = datetime.today() - timedelta(days=1)
            month = months[yesterday.month - 1]
            dateStr = yesterday.strftime("%d. " + month)

        elif "uden afgift" in dateTmp.lower():
            dateStr = "N/A"

        else:
            dateStr = dateTmp.split(" kl.")[0]

        images = self.driver.find_elements_by_class_name("thumb-printable")

        imageLinks = []

        for img in images:
            imageLinks.append(img.get_attribute("src"))

        self.importData(price, linkUrl, zip, area, dateStr, imageLinks)

    def dbResetActive(self):
        mycursor = self.mydb.cursor()
        sql = "UPDATE scrapedCars set active = 0 WHERE 0 = 0"
        mycursor.execute(sql)
        self.mydb.commit()

    def dbSetActive(self, linkUrl):
        mycursor = self.mydb.cursor()
        sql = "UPDATE scrapedCars set active = 1 WHERE link = '"+linkUrl+"'"
        mycursor.execute(sql)
        self.mydb.commit()

    def dbDeleteInactive(self):
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM scrapedCars where active = 0"
        mycursor.execute(sql)
        self.mydb.commit()

    def importData(self, price, link, zip, area, dateStr, imageLinks):
        mycursor = self.mydb.cursor()

        thumbnail = ""

        try:
            thumbnail = imageLinks[0]
        except:
            thumbnail = " "

        imagesStr = ""

        for img in imageLinks:
            imagesStr += "" + img + ", "

        sql = "INSERT INTO scrapedCars (price, link, thumbnail, imagelinks, zipcode, area, active, listingdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (price, link, thumbnail, imagesStr, zip, area, 1, dateStr)
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
    temp.openPage("https://www.dba.dk/biler/biler/reg-aalborg/?fra=privat&sort=listingdate-desc")
    temp.dbDeleteInactive()

