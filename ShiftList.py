from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFormLayout, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200,200,1200,600)
        self.setWindowTitle("Shift List Maker")
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # layouts
        self.main_layout = QVBoxLayout()
        self.form_layout = QVBoxLayout()

        # Error label
        self.error_label = QLabel("")

        # Input field for number of workers
        self.label_num_workers = QLabel("Počet pracovníkov:")
        self.input_num_workers = QLineEdit()
        self.input_num_workers.setValidator(QIntValidator())
        self.input_num_workers.setMaxLength(3)
        self.input_num_workers.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.input_num_workers.setFont(QFont("Arial", 20))
        
        # Input field for number of days
        self.label_num_days = QLabel("Počet dní v mesiaci:")
        self.input_num_days = QLineEdit()
        self.input_num_days.setValidator(QIntValidator())
        self.input_num_days.setMaxLength(3)
        self.input_num_days.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.input_num_days.setFont(QFont("Arial", 20))

        # Button to draw table
        self.createButton = QPushButton("Vytvoriť tabuľku")
        self.createButton.clicked.connect(self.createTable)

        # Table widget (empty initially)
        self.tableWidget = QTableWidget()

        # Button to fill table with shifts
        self.generateButton = QPushButton("Doplniť zmeny")
        self.generateButton.clicked.connect(self.generateShifts)

        # adding input fields to the form layout
        self.form_layout.addWidget(self.error_label)
        self.form_layout.addWidget(self.label_num_workers)
        self.form_layout.addWidget(self.input_num_workers)
        self.form_layout.addWidget(self.label_num_days)
        self.form_layout.addWidget(self.input_num_days)

        # adding everything to the main layout
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.createButton)
        self.main_layout.addWidget(self.tableWidget)
        self.main_layout.addWidget(self.generateButton)
        
        self.centralWidget.setLayout(self.main_layout)

    def createTable(self):
        try:
            num_workers = int(self.input_num_workers.text())
            num_days = int(self.input_num_days.text())

            if num_workers <= 0 or num_days <= 0:
                raise ValueError
            
            # set table size
            self.tableWidget.setRowCount(num_workers)
            self.tableWidget.setColumnCount(num_days + 1)

            # set headers
            column_headers = ["Meno"]
            for i in range(num_days):
                column_headers.append(str(i + 1))
            self.tableWidget.setHorizontalHeaderLabels(column_headers)

            self.error_label.setText("Tabuľka úspešne vytvorená :)")
            
        except ValueError:
            self.error_label.setText("Zadané číslo je nesprávne!")

    def generateShifts(self):
        self.label.setText("You pressed the button !")
        self.update()
    
    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec ())

window()
