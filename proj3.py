"""

Fall 2017 CSC 690

File: proj3.py
By: Kanakapriya Krishnakumar
Last Edited: 10/21/2017

Compile: python3 Main.py  W
    where w is an int for the size of the window, preferred 800


Description: Allows user to specify width of the main display, displays 5 images which can be browsed
through using up, down, right, left, greater than, and less than keys. Can also add and save 
tags based on what images it is saved in. Creates a text file with the name of the image the tag was added
in.

Additional Advantages: Uses Flickr to browse images. Contains: Search, Save, Test, Delete, Exit Functions for the 
convinence of user. 

"""

import sys
import os
import model

from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

import json
import requests
import ntpath

from os.path import basename

        

class ClickableLabel(QLabel):

    clicked = pyqtSignal(QLabel)
    
    def __init(self, parent):
        self.name = None
        self.next = None
        self.prev = None
        

        super().__init__(parent)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self)


def resizePicture(self, pixmap, border):
        if pixmap.height() >= pixmap.width():

            pixmap = pixmap.scaledToHeight(self.height() - (2 * border))
            self.setPixmap(pixmap)
            self.setAlignment(Qt.AlignCenter)

        else:
            pixmap = pixmap.scaledToWidth(self.width() - (2 * border))
            self.setPixmap(pixmap)
            self.setAlignment(Qt.AlignCenter)


class Window(QWidget):
 
    def __init__(self,width):
        super().__init__()
        self.title = 'PyQt5 Project 3'
        self.initUI()

    def initUI(self):


        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color: black")

        #MAIN DISPLAY WINDOW WIDTH

        #Setting up width and height based on the parameter given in command line
        widthParameter = sys.argv[1]
        w = int(widthParameter)
        h = w * .75
        self.setGeometry(100, 100, w, h)


        #AUDITORY ICONS

        #Sound effect for every key/ mouse click occuring
        self.sound1 = QSoundEffect()
        self.sound1.setSource(QUrl.fromLocalFile(os.path.join('sounds','cp2poing.wav')))
        self.sound2 = QSoundEffect()
        self.sound2.setSource(QUrl.fromLocalFile(os.path.join('sounds',"TRN_PASS.WAV")))


        #Creating a list to store all the tags of the current image, setting up mode, cursor, and index
        self.list = []
        self.data = model.model()

        self.mode = 0 
        self.cursor = None 
        self.index = 1 
        
        
        #SETTING UP LABELS

        #LABEL 1
        self.label1 = ClickableLabel(self)

        #setting up the look of the label
        self.label1.resize(w*.2,h*.2) 
        self.label1.move(0, (w/5))

        #setting the cursor at label 1 to begin the browsing
        self.cursor = self.label1

        #enabling mouse events
        self.label1.clicked.connect(self.mouseSel)


        #LABEL 2
        self.label2 = ClickableLabel(self)

        #setting up previous and next node
        self.label2.prev = self.label1
        self.label1.next = self.label2

        #setting up the look of the label
        self.label2.resize(w*.2,h*.2)
        self.label2.move(157,(w/5))

        #enabling mouse events
        self.label2.clicked.connect(self.mouseSel)


        #LABEL 3
        self.label3 = ClickableLabel(self)

        #setting up previous and next node
        self.label3.prev = self.label2
        self.label2.next = self.label3

        #setting up the look of the label
        self.label3.resize(w*.2,h*.2)
        self.label3.move(314,(w/5))

        #enabling mouse events
        self.label3.clicked.connect(self.mouseSel)


        #LABEL 4
        self.label4 = ClickableLabel(self)

        #setting up previous and next node
        self.label4.prev = self.label3
        self.label3.next = self.label4

        #setting up the look of the label
        self.label4.resize(w*.2,h*.2)
        self.label4.move(471,(w/5))

        #enabling mouse events
        self.label4.clicked.connect(self.mouseSel)

        #LABEL 5
        self.label5 = ClickableLabel(self)

        #setting up previous and next node
        self.label5.prev = self.label4
        self.label4.next = self.label5
        self.label5.next = self.label1
        self.label1.prev = self.label5

        #setting up the look of the label        
        self.label5.resize(w*.2,h*.2)
        self.label5.move(628,(w/5))

        #enabling mouse events
        self.label5.clicked.connect(self.mouseSel)
 

        #LABEL 6 (set to be invisible)
        self.label6 = ClickableLabel(self)

        #setting up the look of the label
        self.label6.resize(self.width()-100, self.height()-100)
        self.label6.move(0,0)

        #enabling mouse events
        self.label6.clicked.connect(self.mouseSel)

        #Uploads pictures that are currently in Data Folder
        self.updatePicture()

        
        #SETTING UP TEXT ANNOTATIONS

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(0, 600)
        self.textbox.setStyleSheet("background-color: white")
        self.textbox.resize(200,40)
 
        #Create a box where tags are listed
        self.tags = QLabel(self)
        self.tags.move(820,0)
        self.tags.setStyleSheet('border: 5px solid grey')
        self.tags.resize(40,400)

        # Create a button in the window
        self.button1 = QPushButton('Save Tag', self)
        self.button1.move(200,600)
        self.button1.setStyleSheet("background-color: white")
        self.button1.clicked.connect(self.click1)

        # Create a button in the window
        self.button2 = QPushButton('Save All Tags', self)
        self.button2.setStyleSheet("background-color: white")
        self.button2.move(300,600)
        self.button2.clicked.connect(self.click2)

        
        #UI ACTION BUTTONS

        # Create textbox
        self.searchbox = QLineEdit(self)
        self.searchbox.move(10, 500)
        self.searchbox.setStyleSheet("background-color: white")
        self.searchbox.resize(200,23)

        
        #SEARCH Button
        self.search = QPushButton('Search', self)
        self.search.move(220, 500)
        self.search.setStyleSheet("background-color: white")
        self.search.clicked.connect(self.searchClick)

        #Create testbox
        self.resultbox = QLineEdit('5',self)
        self.resultbox.move(350, 500)
        self.resultbox.setStyleSheet("background-color: white")
        self.resultbox.resize(80, 23)

        #Setting a text
        self.label = QLabel(self)
        self.label.setText('Max Search Result')
        self.label.setStyleSheet("background-color: white")
        self.label.move(450, 500)
        

        #TEST Button
        self.test = QPushButton('Test', self)
        self.test.move(10,530)
        self.test.setStyleSheet("background-color: white")
        self.test.clicked.connect(self.testClick)

        #SAVE Button
        self.save = QPushButton('Save', self)
        self.save.move(90,530)
        self.save.setStyleSheet("background-color: white")
        self.save.clicked.connect(self.saveClick)

        #EXIT Button
        self.exit = QPushButton('Exit', self)
        self.exit.move(170, 530)
        self.exit.setStyleSheet("background-color: white")
        self.exit.clicked.connect(self.exitClick) 

        #DELETE Button
        self.delete = QPushButton('Delete', self)
        self.delete.move(250, 530)
        self.delete.setStyleSheet("background-color: white")
        self.delete.clicked.connect(self.deleteClick)
    
       
        self.updateView()
        self.show()


    #Search Function
    def searchClick(self):

        #Print on terminal what is being searched and how many pictures
        print("search")
        print (self.searchbox.text())
        print (self.resultbox.text())

        #Makes sure search value is not empty and sets num of pics 5 if no value is inputed 
        if self.searchbox.text() != "": 
            maxNum = "5"
            if self.resultbox.text() != "":
               maxNum = self.resultbox.text()
            else:
                self.resultbox.text().setText("5")

        #Flickr SEARCH
        req = 'https://api.flickr.com/services/rest/'
        req = req + '?method=flickr.photos.search'
        req = req + '&per_page='+ maxNum
        req = req + '&format=json&nojsoncallback=1&extras=geo'
        req = req + '&api_key=0d0003cfc8566a5f4d002135d08bad1a'
        req = req + '&tags='+ self.searchbox.text()

        jsonRespDict = requests.get(req).json()
        rr = jsonRespDict['photos']

        for p in rr['photo']:
            print(p['title'])
            farm = str(p['farm'])
            server = str(p['server'])
            id = str(p['id'])
            secret = str(p['secret'])
            url = "http://farm"+farm+".static.flickr.com/"+server+"/"+id+"_"+secret+".jpg"
            
            print(url)

            url_data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            name = ntpath.basename(url)
            pixmap.loadFromData(url_data)
            pixmap.save(os.path.join("./data", name))


            print("\n")


        self.data = model.model()
        self.index = self.data.position(name)
        self.cursor = self.label1
        self.updatePicture()
        self.searchbox.setText("")
        self.setFocus()
       
    #Test Function
    def testClick(self):
        print("test")
        if self.searchbox.text() != "":
            path = self.searchbox.text()
            self.searchbox.setText("")

            url_data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(url_data)
            name = ntpath.basename(url)
            pixmap.save(os.path.join("./data", name))
            

            self.data = model.model()
            self.index = self.data.position(name)
            self.cursor = self.label1
            self.updatePicture()
       

    #Save Function
    def saveClick(self):
        print("save")

    #Exit Function
    def exitClick(self):
        print("exit")
        self.close()

    #Delete Function
    def deleteClick(self):
        print("delete")
        index = self.cursor.name
        name = self.data.list[index].data
        os.remove("data/"+name)
        
        #check for tags file
        self.cursor.Name = os.path.splitext(self.data.list[self.cursor.name].data)[0]
        filename = (self.cursor.Name +".txt")
        if os.path.isfile(filename):
            os.remove(filename)
        self.setFocus()
        self.data = model.model()
        self.updatePicture()
    

    #MOUSE EVENT
    def mouseSel(self, label):
        self.sound1.play()

        if self.mode == 0:
            self.mode = 1
            self.cursor = label
            self.updateView()

        else:
            self.mode = 0
            self.updateView()


    #KEY EVENT     
    def keyPressEvent(self, event):

        #LEFT ARROW
        if(event.key() == 16777234):
            self.sound1.play()
            if(self.cursor == self.label1):
                self.loadLeft()
                self.updateView()

            else:
                self.cursor = self.cursor.prev
                self.updateView()

        #RIGHT ARROW
        elif(event.key()== 16777236):
            self.sound1.play()

            if(self.cursor == self.label5):
                self.loadRight()
                self.updateView()

            else:
                self.cursor = self.cursor.next
                self.updateView()

        #UP ARROW
        elif(event.key() == 16777235 and self.mode  == 0):
            self.sound1.play()
            self.mode = 1
            self.updateView()
        

        #DOWN ARROW
        elif(event.key() == 16777237 and self.mode == 1):
            self.sound1.play()
            self.mode = 0
            self.updateView()


        #'>' KEY
        elif(event.key() == 46):
            self.sound2.play()
            self.cursor = self.label5
            self.loadRight()
            self.cursor = self.label1
            self.updateView()


        #'<' KEY
        elif(event.key() == 44):
            self.sound2.play()
            self.cursor = self.label1
            self.loadLeft()
            self.cursor = self.label1
            self.updateView()


    #LOADS PRVIOUS FIVE PICTURES
    def loadLeft(self):      
        self.cursor = self.label5
        self.cursor.setStyleSheet('border: 5px solid red')      
        self.index = self.index - 5
        self.updatePicture()
        

    #LOADS NEXT FIVE PICTURES
    def loadRight(self):     
        self.cursor = self.label1
        self.cursor.setStyleSheet('border: 5px solid red')
        self.index = self.index + 5
        self.updatePicture()

    
    #UPDATES THE LABELS, ON WHICH TO SHOW
    def updateView(self):
        self.list = []
        self.getTags()
        self.setFocus()

        if self.mode == 0:
            self.label1.setVisible(1)
            self.label2.setVisible(1)
            self.label3.setVisible(1)
            self.label4.setVisible(1)
            self.label5.setVisible(1)
            self.label6.setVisible(0)
            
            self.search.setVisible(1)
            self.test.setVisible(1)
            self.save.setVisible(1)
            self.delete.setVisible(1)
            self.exit.setVisible(1)

            self.searchbox.setVisible(1)
            self.resultbox.setVisible(1)
            self.label.setVisible(1)
            
            self.button1.setVisible(0)
            self.button2.setVisible(0)
            self.textbox.setVisible(0)
            self.tags.setVisible(0)
            
           
        else:
            self.label1.setVisible(0)
            self.label2.setVisible(0)
            self.label3.setVisible(0)
            self.label4.setVisible(0)
            self.label5.setVisible(0)
            self.label6.setVisible(1)

            self.search.setVisible(0)
            self.test.setVisible(0)
            self.save.setVisible(0)
            self.delete.setVisible(0)
            self.exit.setVisible(0)

            self.searchbox.setVisible(0)
            self.resultbox.setVisible(0)
            self.label.setVisible(0)
            
            self.button1.setVisible(1)
            self.button2.setVisible(1)
            self.textbox.setVisible(1)
            self.tags.setVisible(1)

        self.label1.setStyleSheet('border: 5px solid gray')
        self.label2.setStyleSheet('border: 5px solid gray')
        self.label3.setStyleSheet('border: 5px solid gray')
        self.label4.setStyleSheet('border: 5px solid gray')
        self.label5.setStyleSheet('border: 5px solid gray')
        self.cursor.setStyleSheet('border: 5px solid red')
    
        n = self.cursor.name
        pic = QPixmap("data/"+self.data.list[n].data)
        resizePicture(self.label6,pic, 20)

        
    #Adding the tag
    def click1(self):
        textboxValue= self.textbox.text()
        self.list.append(textboxValue)
        self.textbox.setText("")
        self.setFocus()
        
    #Saving Tag in a txt file
    def click2(self):
        self.cursor.Name = os.path.splitext(self.data.list[self.cursor.name].data)[0]
        filename = (self.cursor.Name+".txt")
        f = open(filename,"a+")
        for i in (self.list):
             f.write(i + "\n")
        self.list = []
        self.setFocus()
        self.getTags()
        self.updateView()


    # Collecting and displaying tags 
    def getTags(self):
        self.tags.clear()
        self.tags.setStyleSheet("background-color: white")

        self.cursor.Name = os.path.splitext(self.data.list[self.cursor.name].data)[0]

        filename = (self.cursor.Name+".txt")
        text = "TAGS: \n"

        if os.path.isfile(filename):
            f = open(filename,"r")
            tags = f.readlines()
            for x in tags:
                text = text + x
        self.tags.setText(text)

        
    #Updates the pictures each time there is an UI function or key event
    def updatePicture(self):
        
        self.label1.name = self.data.get(self.index).id
        pic = QPixmap("data/"+self.data.get(self.index).data)
        resizePicture(self.label1,pic,5)

        self.label2.name = self.data.get(self.index+1).id
        pic = QPixmap("data/"+self.data.get(self.index+1).data)
        resizePicture(self.label2,pic,5)

        self.label3.name = self.data.get(self.index+2).id
        pic = QPixmap("data/"+self.data.get(self.index+2).data)
        resizePicture(self.label3,pic,5)

        self.label4.name = self.data.get(self.index+3).id
        pic = QPixmap("data/"+self.data.get(self.index+3).data)
        resizePicture(self.label4,pic,5)

        self.label5.name = self.data.get(self.index+4).id
        pic = QPixmap("data/"+self.data.get(self.index+4).data)
        resizePicture(self.label5,pic, 5)


 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window(sys.argv[1])
    sys.exit(app.exec_())
