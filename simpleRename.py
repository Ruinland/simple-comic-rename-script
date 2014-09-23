import imghdr
import os
from os import listdir
from os.path import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


leagalPicType = ['gif','jpeg','bmp','png']

def isPic(filenameWithPath):
    if imghdr.what(filenameWithPath) in leagalPicType:
        return True

class workingWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self, windowTitle="A Simple Pic Renaming Tool.")
        self.fileList = [ fileCur for fileCur in listdir(".") if isPic(join(".",fileCur))]
        self.fileList.sort()


        grid = QVBoxLayout()
        hbox = QHBoxLayout()


        self.currListFile = ""
        self.pendingList = []

        self.renameButton=QPushButton("Rename them(&R)", self)
        self.renameButton.clicked.connect(self.doRename)

        self.putToPending=QPushButton("===>(&K)", self)
        self.putToPending.clicked.connect(self.doPutPending)

        self.putUp=QPushButton("↑(&U)", self)
        self.putUp.clicked.connect(self.doPutUp)

        self.putDown=QPushButton("↓(&I)", self)
        self.putDown.clicked.connect(self.doPutDown)

        self.removeFromPending=QPushButton("<===(&J)", self)
        self.removeFromPending.clicked.connect(self.doRemovePending)

        grid.layout().addWidget(self.putToPending)
        grid.layout().addWidget(self.removeFromPending)
        grid.layout().addWidget(self.putUp)
        grid.layout().addWidget(self.putDown)
        grid.layout().addWidget(self.renameButton)
        
        self.picList = QListWidget(self)
        self.picList.addItems(self.fileList)
        self.picList.setCurrentRow(0)
        self.picList.currentItemChanged.connect(self.onItemChanged)

        self.changeList = QListWidget(self)
        self.changeList.currentItemChanged.connect(self.onItemChanged)

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setPixmap(QtGui.QPixmap(self.fileList[0]))

        hbox.layout().addWidget(self.picList)
        hbox.layout().addWidget(self.changeList)
        hbox.addLayout(grid)
        hbox.layout().addWidget(self.lbl)

        self.setLayout(hbox)


    def doPutUp(self):
        idx = self.changeList.currentRow()
        curr = self.changeList.takeItem(idx)
        self.changeList.insertItem(idx-1,curr)
        self.changeList.setCurrentRow(idx-1)

    def doPutDown(self):
        idx = self.changeList.currentRow()
        curr = self.changeList.takeItem(idx)
        self.changeList.insertItem(idx+1,curr)
        self.changeList.setCurrentRow(idx+1)


    def doPutPending(self):
        idx = self.picList.currentRow()
        whatRemove = self.picList.takeItem(idx)
        self.changeList.addItem(whatRemove)

    def doRemovePending(self):
        idx = self.changeList.currentRow()
        whatPutBack = self.changeList.takeItem(idx)
        self.picList.addItem(whatPutBack)
        self.picList.sortItems()

    def onItemChanged(self,curr,prev):
        if curr != None :
            self.lbl.setPixmap(QtGui.QPixmap(curr.text()))
            self.currListFile = curr.text()

    def doRename(self):
        for listIter in range(0,self.changeList.count()) :
            fileName = self.changeList.item(listIter).text()
            self.pendingList.append(fileName)
        for idx, nameIter in enumerate(self.pendingList) :
            fN , subFn = os.path.splitext(nameIter)
            cmd = ["mv",nameIter,"comic-"+str(idx)+subFn]
            os.system(" ".join(cmd))


        self.changeList.clear()
        self.fileList = [ fileCur for fileCur in listdir(".") if isPic(join(".",fileCur))]
        self.fileList.sort()
        self.picList.clear()
        self.picList.addItems(self.fileList)
        self.picList.setCurrentRow(0)

app=QApplication(sys.argv)
workWidget=workingWidget()
workWidget.show()
sys.exit(app.exec_())
