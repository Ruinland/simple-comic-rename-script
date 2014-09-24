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
    if os.path.isfile(filenameWithPath):
        if imghdr.what(filenameWithPath) in leagalPicType:
            return True

class workingWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self, windowTitle="A Simple Pic Renaming Tool.")
        self.fileList = [ fileCur for fileCur in listdir(".") if isPic(join(".",fileCur))]
        self.fileList.sort()


        grid = QBoxLayout(QBoxLayout.TopToBottom)
        hbox = QHBoxLayout()


        self.currListFile = ""
        self.pendingList = []

        self.renameButton=QPushButton("Rename them(&R)", self)
        self.renameButton.clicked.connect(self.doRename)
        self.renameButton.setMaximumWidth(100)

        self.putToPending=QPushButton("===>(&K)", self)
        self.putToPending.clicked.connect(self.doPutPending)
        self.putToPending.setMaximumWidth(100)

        self.putUp=QPushButton("↑(&U)", self)
        self.putUp.clicked.connect(self.doPutUp)
        self.putUp.setMaximumWidth(100)

        self.putDown=QPushButton("↓(&I)", self)
        self.putDown.clicked.connect(self.doPutDown)
        self.putDown.setMaximumWidth(100)

        self.removeFromPending=QPushButton("<===(&J)", self)
        self.removeFromPending.clicked.connect(self.doRemovePending)
        self.removeFromPending.setMaximumWidth(100)

        grid.layout().addWidget(self.putToPending)
        grid.layout().addWidget(self.removeFromPending)
        grid.layout().addWidget(self.putUp)
        grid.layout().addWidget(self.putDown)
        grid.layout().addWidget(self.renameButton)
        
        self.picList = QListWidget(self)
        self.picList.setMaximumWidth(200)
        self.picList.addItems(self.fileList)
        self.picList.setCurrentRow(0)
        self.picList.currentItemChanged.connect(self.onItemChanged)

        self.changeList = QListWidget(self)
        self.changeList.setMaximumWidth(200)
        self.changeList.currentItemChanged.connect(self.onItemChanged)

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setMaximumSize(500,700)
        if self.picList.count() > 0 :
            self.lbl.setPixmap(QtGui.QPixmap(self.fileList[0]).scaled(500,700))

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
            self.lbl.setPixmap(QtGui.QPixmap(curr.text()).scaled(500,700))
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


if __name__ == "__main__":
    app=QApplication(sys.argv)
    workWidget=workingWidget()
    workWidget.show()
    sys.exit(app.exec_())
