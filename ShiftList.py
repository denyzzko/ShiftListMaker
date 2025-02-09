from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200,200,300,300)
        self.setWindowTitle("Shift List Maker")
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.label = QtWidgets.QLabel(self)
        self.label.setText("This is Label")
        self.label.move(50,50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Generate")
        self.b1.clicked.connect(self.button_clicked)

        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.b1)
        
        self.centralWidget.setLayout(self.layout)

    def createTable(self):
        self.tableWidget = QTableWidget()
        #row count
        self.tableWidget.setRowCount(4)
        #column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0,0, QTableWidgetItem("Name")) 
        self.tableWidget.setItem(0,1, QTableWidgetItem("City")) 
        self.tableWidget.setItem(1,0, QTableWidgetItem("Aloysius")) 
        self.tableWidget.setItem(1,1, QTableWidgetItem("Indore")) 
        self.tableWidget.setItem(2,0, QTableWidgetItem("Alan")) 
        self.tableWidget.setItem(2,1, QTableWidgetItem("Bhopal")) 
        self.tableWidget.setItem(3,0, QTableWidgetItem("Arnavi")) 
        self.tableWidget.setItem(3,1, QTableWidgetItem("Mandsaur"))

    def button_clicked(self):
        self.label.setText("You pressed the button")
        self.update()
    
    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec ())

window()
