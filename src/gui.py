import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QProgressBar, QListWidget, QGridLayout, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from search import *

TIME_LIMIT = 2


class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):
        count = 0
        loader = LoadFiles()
        loader.run()
        while count < TIME_LIMIT:
            count += 0.5
            time.sleep(0.5)
            self.countChanged.emit(count)


class LoadFiles:
    def run(self):
        load_index()
        return 1

class Ui_DockWidget(object):
    def __init__(self):
        self.calc = External()


    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(900, 600)
        DockWidget.move(350, 150)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        DockWidget.setPalette(palette)
        DockWidget.setAutoFillBackground(False)
        DockWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "")
        DockWidget.setFloating(False)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.searchBox = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.searchBox.setGeometry(QtCore.QRect(210, 270, 450, 51))
        self.searchBox.setStyleSheet("border-color: rgb(85, 0, 127);\n"
                                     "background-color: rgb(255, 255, 255);")
        self.searchBox.setText("")
        self.searchBox.setDragEnabled(True)
        self.searchBox.setObjectName("lineEdit")
        self.searchButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.searchButton.setGeometry(QtCore.QRect(210 - 91 / 2 + 450 / 2, 340, 91, 41))
        self.searchButton.setStyleSheet("color: rgb(255, 0, 127);")
        self.searchButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(350, 80, 170, 170))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../images/query.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")


        self.docs_result = QtWidgets.QTextBrowser(self.dockWidgetContents)
        self.docs_result.setGeometry(187,400,500,80)
        self.docs_result.hide()
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

        self.setEvents()


        self.progress = QProgressBar(self.dockWidgetContents)
        self.progress.setGeometry(250, 500, 350, 25)
        self.progress.setMaximum(2)
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setToolTip(_translate("DockWidget", "<html><head/><body><p>dd</p><p><br/></p></body></html>"))
        DockWidget.setWindowTitle(_translate("DockWidget", "Searchly"))

        self.searchButton.setText(_translate("DockWidget", "SEARCH"))

    def setEvents(self):
        self.searchButton.clicked.connect(self.on_search_click)

    def onCountChanged(self, value):
        self.progress.setValue(value)


    def on_search_click(self):
        query = self.searchBox.text()
        result = process_query(query)
        result = ','.join(str(x) for x in result)
        print(result)
        self.docs_result.show()
        self.docs_result.setText(result)
        print(result)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DockWidget = QtWidgets.QDockWidget()
    ui = Ui_DockWidget()
    ui.setupUi(DockWidget)
    DockWidget.show()
    sys.exit(app.exec_())

