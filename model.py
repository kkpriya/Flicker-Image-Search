"""

Fall 2017 CSC 690

File: model.py
By: Kanakapriya Krishnakumar
Last Edited: 10/21/2017

Compile: python3 Main.py  W
    where w is an int for the size of the window


Description: This file shows the data model, getting images, setting the nodes for each labels, calling for
previous and next labels
"""


import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class list:
    def __init__(self, data, id, next, prev):   
        self.data = data    
        self.id = id        
        self.next = next    
        self.prev = prev    

class model():

    def __init__(self):
        
        #CREATING A LIST TO STORE AND COLLECT ALL IMAGES IN THE DATA FOLDER
        self.list = []
        lists = (os.listdir(os.path.join('.','data')))
        
        for file in lists:

            if len(self.list)==0:
                #if there is none stored in the list 
                self.list.append(list(file,0,None,None))

            else:
                #getting previous and next node
                self.list.append(list(file,(len(self.list)),self.list[0],self.list[len(self.list)-1]))
                self.list[0].prev = self.list[len(self.list)-1]
                self.list[len(self.list)-2].next = self.list[len(self.list)-1]

        
    def get(self, index):

        length = len(self.list)

        if index < 0:
            i = self.list[(length-1)]
            while(length > index):
                i = i.next
                length = length - 1
            return i

        elif index < length:
            return self.list[index]

        else:
            length = self.list[0]
            while(length < index):
                length = i.next
                length = length + 1
            return i
                
    #getting the position of the node
    def position(self, data):
        for node in self.list:
            if data == node.data:
                return node.id
   
        

