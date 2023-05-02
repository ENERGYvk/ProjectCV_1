from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import random
from PIL import Image, ImageTk
import pytesseract
import matplotlib.pyplot as plt
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

def openImg(pathImg):
    tempImg = cv2.imread(pathImg)
    tempImg = cv2.cvtColor(tempImg, cv2.COLOR_BGR2RGB)
    # plt.imshow(tempImg)
    # plt.axis('off')
    # plt.show()

    return tempImg

def extract(image,model):
    rects = model.detectMultiScale(image,scaleFactor=1.1, minNeighbors=5)
    for x,y,w,h in rects:
        carpalte_img = image[y+15:y+h-10,x+15:x+w]

    return carpalte_img

def enalarge_img(image,percent):
    width = int(image.shape[1]*percent/100)
    height = int(image.shape[0]*percent/100)
    dim = (width,height)
    # plt.axis('off')
    resized_img = cv2.resize(image,dim,interpolation=cv2.INTER_AREA)

    return resized_img

class MyWidget(GridLayout):

    def selected(self,filename):
        try:
            # print(filename[0])

            img=filename[0]
            model = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
            tempimg = openImg(img)
            tempimg = extract(tempimg, model)
            tempimg = enalarge_img(tempimg, 150)
            # plt.imshow(tempimg)
            # plt.show()
            tempimg_grey = cv2.cvtColor(tempimg, cv2.COLOR_RGB2GRAY)
            # plt.axis('off')
            # plt.imshow(tempimg_grey, cmap='gray')
            # plt.show()

            number = pytesseract.image_to_string(tempimg_grey,
            config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            self.ids.textbox.text = number
            self.ids.image.source = filename[0]
        except:
            pass

class FileChoose(App):

    def build(self):
        return MyWidget()


if __name__ == "__main__":
    window = FileChoose()
    window.run()