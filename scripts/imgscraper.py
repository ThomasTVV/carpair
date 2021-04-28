import mysql.connector
import requests
import re

class ImgDownloader():
   
    def __init__(self):
        self.mydb = mysql.connector.connect(
                host="mysql112.unoeuro.com",
                user="sikkermail_konsulent_dk",
                password="zrdEhaktw2g9",
                database="sikkermail_konsulent_dk_db"
            )

    def GetURLFromDB(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT id, imagelinks from scrapedCars"
        mycursor.execute(sql)
        ImageURLs = mycursor.fetchall()
        self.DownloadImgFromUrl(ImageURLs)

    def DownloadImgFromUrl(self, ImageURLs):
        status = None
        try:
            carNum = 0
            for imageData in ImageURLs:
                imgNum = 0
                carNum += 1
                carID = imageData[0]
                imagelinks = imageData[1].strip().split(',')
                imagelinks.pop() # last element returns empty, because it splits at ',' and last charchter is ','
                for element in imagelinks:
                    print(element)
                    imgNum += 1
                    filename = str(carNum) + "-" + str(carID) + "-" + str(imgNum) + ".jpg"
                    img = requests.get(element).content # <-- this should be printed, but 
                    with open(filename, 'wb') as handler:
                        handler.write(img)
        except ValueError:
            pass 
        finally:
            if status != 200:
                print("error")
            else:
                print("awesome")

if __name__ == '__main__':
    ImgDownloader().GetURLFromDB()