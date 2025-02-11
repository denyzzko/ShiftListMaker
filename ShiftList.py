from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFormLayout, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout,
    QMenuBar, QMenu
)
from PyQt6.QtGui import QIntValidator, QFont, QAction
from PyQt6.QtCore import Qt, QCoreApplication
import sys
import json

JSON_FILE = "shifts.json"

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200,200,1200,600)
        self.setWindowTitle("Shift List Maker")
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.form_layout = QVBoxLayout()
        self.menu_layout = QHBoxLayout()

        # Top menu bar (NOT COMPLETED YET -- TODO REST OF MENU SECTIONS AND SHORTCUTS)
        self.menubar = QMenuBar()
        _translate = QCoreApplication.translate
        
        self.menuFile = self.menubar.addMenu("File")
        self.menuEdit = self.menubar.addMenu("Edit")
        self.menuView = self.menubar.addMenu("View")
        self.menuHelp = self.menubar.addMenu("Help")

        self.actionNew = QAction("New", self)
        self.actionNew.triggered.connect(self.createTable)
        self.menuFile.addAction(self.actionNew)
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        
        self.menuFile.addAction("Open")
        
        self.actionSave = QAction("Save", self)
        self.actionSave.triggered.connect(self.storeToJSON)
        self.menuFile.addAction(self.actionSave)
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        
        self.actionLoad = QAction("Load", self)
        self.actionLoad.triggered.connect(self.loadFromJSON)
        self.menuFile.addAction(self.actionLoad)
        self.actionLoad.setShortcut(_translate("MainWindow", "Ctrl+L"))

        self.menuFile.addSeparator()
        
        self.menuFile.addAction("Quit")

        # Add menu bar to the menu layout
        self.menu_layout.addWidget(self.menubar)
  
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

        # Adding input fields to the form layout
        self.form_layout.addWidget(self.error_label)
        self.form_layout.addWidget(self.label_num_workers)
        self.form_layout.addWidget(self.input_num_workers)
        self.form_layout.addWidget(self.label_num_days)
        self.form_layout.addWidget(self.input_num_days)

        # Adding everything to the main layout
        self.main_layout.addLayout(self.menu_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.createButton)
        self.main_layout.addWidget(self.tableWidget)
        self.main_layout.addWidget(self.generateButton)
        
        self.centralWidget.setLayout(self.main_layout)

    # Function to draw table on screen
    def createTable(self):
        try:
            num_workers = int(self.input_num_workers.text())
            num_days = int(self.input_num_days.text())

            if num_workers <= 0 or num_days <= 0:
                raise ValueError
            
            # Set table size
            self.tableWidget.setRowCount(num_workers)
            self.tableWidget.setColumnCount(num_days + 1)

            # Set headers
            column_headers = ["Meno"]
            for i in range(num_days):
                column_headers.append(str(i + 1))
            self.tableWidget.setHorizontalHeaderLabels(column_headers)

            # Adjust column widths
            self.tableWidget.setColumnWidth(0, 130)  # Wider "Meno" column (150px)
            for col in range(1, num_days + 1):
                self.tableWidget.setColumnWidth(col, 30)  # Narrower shift columns (50px each)

            self.error_label.setText("Tabuľka úspešne vytvorená :)")
            
        except ValueError:
            self.error_label.setText("Zadané číslo je nesprávne!")
    
    # Function to store table content to JSON file
    def storeToJSON(self):
        try:
            # JSON object with data to be stored
            json_object = {
                "num_days":self.tableWidget.columnCount() - 1,
                "num_workers":self.tableWidget.rowCount(),
                "workers":[]
            }

            # Populate JSON object "worker" section from table
            for row in range(self.tableWidget.rowCount()):
                worker_name = self.tableWidget.item(row, 0)
                shifts = []
                for col in range(1, self.tableWidget.columnCount()):
                    shift_item = (self.tableWidget.item(row,col))
                    shifts.append(shift_item.text() if shift_item else "")
                json_object["workers"].append(
                    {
                        "name":worker_name.text() if worker_name else "",
                        "shifts":shifts
                    }
                )
            
            # Open JSON file and write data
            with open(JSON_FILE, "w", encoding="utf-8") as jsonfile:
                json.dump(json_object, jsonfile, indent=4, ensure_ascii=False)
            
            self.error_label.setText("Tabulka uspesne ulozena :)")
            
        except (FileNotFoundError, json.JSONDecodeError):
            self.error_label.setText("Chyba pri ukladani obsahu z tabulky do suboru!")
    
    # Function to load table content from stored JSON file
    def loadFromJSON(self):
        try:
            # Open and get data from JSON file
            with open(JSON_FILE, "r", encoding="utf-8") as jsonfile:
                data = json.load(jsonfile)

            # Insert loaded values to input fields and create table
            self.input_num_days.setText(str(data["num_days"]))   
            self.input_num_workers.setText(str(data["num_workers"]))
            self.createTable()

            # Populate table with loaded json data
            for row, worker in enumerate(data["workers"]):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(worker["name"]))
                for col, shift in enumerate(worker["shifts"], start=1):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(shift))
            
            self.error_label.setText("Tabulka uspesne nacitana :)")
            
        except (FileNotFoundError, json.JSONDecodeError):
            self.error_label.setText("Chyba pri nacitani obsahu ulozenej tabulky!")

    # Function to automatically fill in table with shifts
    def generateShifts(self):
        self.error_label.setText("Tato funkcia este nie je implementovana...")

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec ())

window()
