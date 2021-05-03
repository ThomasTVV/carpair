import mysql.connector
import requests
import os

class ImgDownloader():

   #Mysql credentials
    def __init__(self):
        self.mydb = mysql.connector.connect(
                host="mysql112.unoeuro.com",
                user="sikkermail_konsulent_dk",
                password="zrdEhaktw2g9",
                database="sikkermail_konsulent_dk_db"
            )
            
    #Query database for imglinks
    def GetURLFromDB(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT id, imagelinks from scrapedCars WHERE numberplate IS NULL"
        mycursor.execute(sql)
        ImageURLs = mycursor.fetchall()
        self.DownloadImgFromUrl(ImageURLs)

    #clean data + correctly name files for later handling
    def DownloadImgFromUrl(self, ImageURLs):
        status = None
        save_path = 'C:/Users/simon/Desktop/carpair/anpr/data/images' #save path needs to be changed on other pc's
        try:
            for imageData in ImageURLs:
                imgNum = 0
                carID = imageData[0]
                imagelinks = imageData[1].strip().split(',')
                imagelinks.pop() # last element returns empty, because it splits at ',' and last charchter is ','
                for element in imagelinks:
                    imgNum += 1
                    filename = str(carID) + "-" + str(imgNum) + ".jpg"
                    completeName = os.path.join(save_path, filename)     
                    img = requests.get(element).content
                    with open(completeName, 'wb') as handler:
                        handler.write(img)
        except ValueError:
            pass 
        finally:
            if status != 200:
                print("exited query") #always exits here, even though it sucesfully ran
            else:
                print("awesome")

if __name__ == '__main__':
    ImgDownloader().GetURLFromDB()  