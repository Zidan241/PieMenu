from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os

ButtonLoc = [
    (60, 0), 
    (-60, 0), 
    (0, 60), 
    (0, -60)
]
Apps = [
    (0,'C:\\Program Files\\Google\\Chrome\\Application','chrome.png'),
    (1,'C:\\Program Files\\Mozilla Firefox\\firefox.exe','firefox.png'),
    (2,'C:\\Users\\zidan\\AppData\\Local\\Discord\\Update.exe','discord.png'),
    (3,'C:\\Program Files\\Unity Hub\\Unity Hub.exe','unityhub.ico'),
    (4,'C:\\Program Files (x86)\\Steam','steam.png'),
    (5,'C:\\Users\\zidan','anghami.jpg'),
]
clicked = [
    0,
    0,
    0,
    0,
    0,
    0
]

def takeFirst(elem):
    index, loc, icon = elem
    return clicked[index]

class Button(QtWidgets.QPushButton):
    def __init__(self, index, x, y, icon, loc, parent):
        super().__init__(str(clicked[index]),parent)
        self.setStyleSheet("width: 50px; height: 50px; border-radius: 10px; background-color: #f5f5f5;font-weight: bold;")
        self.index = index
        self.xPos = x
        self.yPos = y
        self.cont = parent
        self.loc = loc
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(30, 30))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            clicked[self.index]+=1
            self.setText(str(clicked[self.index]))
            os.startfile(self.loc)
                # change all buttons
            Apps.sort(key=takeFirst, reverse=True)
            i=0;
            for button in self.cont.menu.buttons:
                tagetIndex = i+self.cont.displayIndex-4
                if button.index != Apps[tagetIndex][0]:
                    button.anim = QtCore.QPropertyAnimation(button, b"geometry")
                    button.anim.setDuration(200)
                    button.anim.setStartValue(QtCore.QRect(button.x(), button.y(), 50, 50))
                    button.anim.setEndValue(QtCore.QRect(65, 65, 50, 50))
                    button.anim.start()

                    index, loc, icon = Apps[tagetIndex]
                    button.setIcon(QtGui.QIcon(icon))
                    button.setText(str(clicked[index]))
                    button.loc = loc
                    button.index = index

                    button.anim = QtCore.QPropertyAnimation(button, b"geometry")
                    button.anim.setDuration(200)
                    button.anim.setStartValue(QtCore.QRect(65, 65, 50, 50))
                    button.anim.setEndValue(QtCore.QRect(65+button.xPos, 65+button.yPos, 50, 50))
                    button.anim.start()
                i+=1

            if self.cont.menu.cent.index != Apps[0][0]:
                index, loc, icon = Apps[0]
                self.cont.menu.cent.setIcon(QtGui.QIcon(icon))
                self.cont.menu.cent.setText(str(clicked[index]))
                self.cont.menu.cent.loc = loc
                self.cont.menu.cent.index = index
        

class CenterButton(QtWidgets.QPushButton):
    def __init__(self, index, icon, loc, parent):
        super().__init__("0", parent)
        self.setStyleSheet("width: 50px; height: 50px; border-radius: 25px; background-color: #C5C5C5;font-weight: bold;")
        self.cont = parent
        self.loc = loc
        self.index = index
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(30, 30))
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)

    def mousePressEvent(self, event):          
        self.oldPos = event.globalPos()
        if event.button() == QtCore.Qt.LeftButton:
            if self.timer.isActive():
                clicked[self.index]+=1
                self.setText(str(clicked[self.index]))
                os.startfile(self.loc)
                self.timer.stop()
            else:
                self.timer.start(250)
  
        elif event.button() == QtCore.Qt.RightButton:
            newDisplayIndex = self.cont.displayIndex;
            i = 0
            for button in self.cont.menu.buttons:
                button.anim = QtCore.QPropertyAnimation(button, b"geometry")
                button.anim.setDuration(200)
                button.anim.setStartValue(QtCore.QRect(button.x(), button.y(), 50, 50))
                button.anim.setEndValue(QtCore.QRect(65, 65, 50, 50))
                button.anim.start()
                newAppIndex = i+self.cont.displayIndex;
                if newAppIndex<len(Apps):
                    index, loc, icon = Apps[newAppIndex]
                    button.setIcon(QtGui.QIcon(icon))
                    button.setText(str(clicked[index]))
                    button.loc = loc
                    button.index = index
                    button.setVisible(True)
                    button.setEnabled(True)
                    newDisplayIndex+=1
                else:
                    button.setVisible(False)
                    button.setEnabled(False)
                button.anim = QtCore.QPropertyAnimation(button, b"geometry")
                button.anim.setDuration(200)
                button.anim.setStartValue(QtCore.QRect(65, 65, 50, 50))
                button.anim.setEndValue(QtCore.QRect(65+button.xPos, 65+button.yPos, 50, 50))
                button.anim.start()
                i+=1
            if newDisplayIndex>=len(Apps):
                self.cont.displayIndex = 1
            else:
                self.cont.displayIndex = newDisplayIndex
                
    def mouseMoveEvent(self, event):
        self.buttonClicked = False
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        self.cont.move(self.cont.x() + delta.x(), self.cont.y() + delta.y())
        self.oldPos = event.globalPos()
        if delta.isNull():
            for button in self.cont.menu.buttons:
                button.anim = QtCore.QPropertyAnimation(button, b"geometry")
                button.anim.setDuration(200)
                button.anim.setStartValue(QtCore.QRect(button.x(), button.y(), 50, 50))
                button.anim.setEndValue(QtCore.QRect(65, 65, 50, 50))
                button.anim.start()
        else:
            for button in self.cont.menu.buttons:
                button.anim = QtCore.QPropertyAnimation(button, b"geometry")
                button.anim.setDuration(200)
                button.anim.setStartValue(QtCore.QRect(65, 65, 50, 50))
                button.anim.setEndValue(QtCore.QRect(65+button.xPos, 65+button.yPos, 50, 50))
                button.anim.start()

    def enterEvent(self, QEvent):
        if self.cont.opened==False:
            self.cont.opened = True;
            for button in self.cont.menu.buttons:
                button.anim = QtCore.QPropertyAnimation(button, b"geometry")
                button.anim.setDuration(200)
                button.anim.setStartValue(QtCore.QRect(self.x(), self.y(), 50, 50))
                button.anim.setEndValue(QtCore.QRect(self.x()+button.xPos, self.y()+button.yPos, 50, 50))
                button.anim.start()
            pass
    
class ContainerButton(QtWidgets.QPushButton):
    opened = False;
    displayIndex = 5;
    def __init__(self, parent):
        super().__init__("",parent)
        self.setStyleSheet('width: 180px; height: 180px; background-color: rgba(255, 255, 255, 0.01);')
        self.menu = parent
    def leaveEvent(self, event):
        self.opened = False;
        for button in self.menu.buttons:
            button.anim = QtCore.QPropertyAnimation(button, b"geometry")
            button.anim.setDuration(200)
            button.anim.setStartValue(QtCore.QRect(button.x(), button.y(), 50, 50))
            button.anim.setEndValue(QtCore.QRect(65, 65, 50, 50))
            button.anim.start()
        pass

class RadialTest(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setStyleSheet("QWidget{background-color: transparent;border:none;}")
        self.setAttribute( QtCore.Qt.WA_TranslucentBackground )
        self.setAttribute( QtCore.Qt.WA_OpaquePaintEvent )
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAcceptDrops(True)

        container = ContainerButton(self)

        self.buttons = []
        for i, (x, y) in enumerate(ButtonLoc):
            index1, loc, icon = Apps[i+1]
            b = Button(index1, x, y, icon, loc, container)
            b.move(65,65)
            self.buttons.append(b)

        index2, loc, icon = Apps[0]
        center = CenterButton(index2, icon, loc, container)
        center.move(65, 65)
        self.cent = center

        self.show()
        self.showFullScreen()

    def buttonClicked(self, id):
        print('Button id {} has been clicked'.format(id))
        
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        self.button.move(position)
        event.accept()

if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    firstScene = RadialTest()
    sys.exit(app.exec_())