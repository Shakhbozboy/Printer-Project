import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageWin
from datetime import datetime
import win32print
import win32print
import win32ui
import json
import time
import uuid



class Printer:
   QRsubPart = None
   def __init__(self, pName, direction) -> None:
      self.pName = pName
      self.pDirection = direction
      font = None
      self.phandle = win32print.OpenPrinter(self.pName)
      print_jobs = win32print.EnumJobs(self.phandle, 0, -1, 1)
      for print_job in print_jobs:
         win32print.SetJob(self.phandle, print_job['JobId'], 1, print_job, win32print.JOB_CONTROL_DELETE)

   def __genQRcode(self, text):
      qr = qrcode.QRCode(version = 1,
                        box_size = 11,
                        border = 3)
      qr.add_data(text)
      qr.make()
      return qr.make_image()


   def __genComeInCheck(self, id):
      now = datetime.now()
      message = f"""                      PARKING            
       Islom Karmiov nomidagi     
     Toshkent Xalqaro aeroporti        
 ----------------------------------------------
 Avtoturargoh:       Uchib kelish   
 ID:                                   {id}
 Kirish vaqti : {now.strftime("%m.%d.%Y, %H:%M")} 
 Tarif(har soat):       10 000 so'm    
        Boshlang'ich 10 daqiqa
                       BEPUL           """
      qr_img = self.__genQRcode(Printer.QRsubPart + id)
      dst = Image.new('RGB', (420, 350 + qr_img.height), color='white')
      dst.paste(qr_img, (-4, 295))
      _ = ImageDraw.Draw(dst).text((20, 0), message, font=Printer.font, fill=(0, 0, 0))
      #dst.show()
      return dst


   def is_content_printed(self, documentName):
      time.sleep(1)
      print_jobs = win32print.EnumJobs(self.phandle, 0, -1, 1)
      for print_job in print_jobs:
         if print_job["pDocument"] == documentName:
            win32print.SetJob(self.phandle, print_job['JobId'], 1, print_job, win32print.JOB_CONTROL_DELETE)
            return False
      return True

      

   def printCheck(self, id):
      image = self.__genComeInCheck(id) #id="ID123456"
      docName = self.__print(image)
      return self.is_content_printed(docName)



   
   def __print(self, image):
      docName = str(uuid.uuid4())[:8]
      hDC = win32ui.CreateDC ()
      hDC.CreatePrinterDC (self.pName)
      hDC.StartDoc (docName)
      hDC.StartPage ()
      image = image.resize((image.width, image.height), Image.Resampling.LANCZOS)
      dib = ImageWin.Dib (image)
      dib.draw (hDC.GetHandleOutput (), (0,0, image.width, image.height))
      hDC.EndPage ()
      hDC.EndDoc ()
      hDC.DeleteDC ()
      return docName

   


printers = dict()
f = open('config.json')
data = json.load(f)
for i in data["printers"]:
    printers[i["ip_camera"]] = Printer(i["pName"], i["direction"])
f.close()
Printer.QRsubPart = data["QRsubPart"]
Printer.font = ImageFont.truetype("fonts\\OpenSans-Bold.ttf", size=24)
#printers["192.168.10.21"].printCheck("AP123456")
#print(printers["192.168.10.21"].is_content_printed("Check"))






