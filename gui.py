from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import sys
# import functions
import networkProcess

class UI(QMainWindow):
	def __init__(self):
		QWidget.__init__(self)
		self.setFixedHeight(600) # autofit table contents and resize the window
		self.setFixedWidth(800)

		self.setWindowTitle('Network Packet Sniffer')
		self.displayMenu()

		self.table_widget = setTable()
		self.widget = QWidget(self)
		layout = QGridLayout()
		self.widget.setLayout(layout)
		layout.addWidget(self.table_widget)

		self.setCentralWidget(self.widget)
		self.scan = False


	def displayMenu(self):
		mainMenu = self.menuBar()

		# Menu Items

		fileMenu = mainMenu.addMenu('File')
		fileMenu.addAction('Export to .csv')
		fileMenu.addAction('Import from .csv')
		
		filterMenu = mainMenu.addMenu('Filter')
		aboutMenu = mainMenu.addMenu('About')

		# Buttons

		startbutton = QPushButton('Start Capturing', self)
		startbutton.clicked.connect(self.onClickStart)
		startbutton.setGeometry(150, 0, 120, 25)

		stopbutton = QPushButton('Stop Capturing', self)
		stopbutton.setGeometry(280, 0, 120, 25)
		stopbutton.clicked.connect(self.onClickStop)

		self.show()

	def runNetworkProcess(self):
		self.thread = QThread()
		self.worker = networkProcess.NetworkProcessWorker()
		self.thread.started.connect(self.worker.run)
		self.worker.packet.connect(self.table_widget.updateTable)

		self.thread.start()

	# Button functions
	
	def onClickStart(self):
		# adds a new row to the table on click of the button

		# self.scan = True
		# connection = networkProcess.getConnection()
		# infinite loop will need to be run in seperate thread instead
		# while self.scan:
			# self.table_widget.updateTable(networkProcess.main(connection))
		# self.table_widget.updateTable(networkProcess.main(connection))
		self.runNetworkProcess()


	def onClickStop(self):
		self.scan = False

# Generate Table

class setTable(QWidget):
	def __init__(self):
		super(setTable, self).__init__()
		self.tableInterface()

	def tableInterface(self):
		self.fetchTable()
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.tableWidget)
		self.setLayout(self.layout)

		self.show()

	def fetchTable(self):
		# make a table with headers
		self.tableWidget = QTableWidget()
		self.tableWidget.setRowCount(0)
		self.tableWidget.setColumnCount(5)
		self.tableWidget.setHorizontalHeaderLabels(['Protocol', 'Source IP', 'Destination IP', 'Source Port', 'Destination port'])
		
		self.tableWidget.setItem(0,0, QTableWidgetItem('test'))  # get items dynamically (functions.py)
		self.tableWidget.resizeColumnsToContents()

	def updateTable(self,row):
		# add a row to the end of the table
		print("________________________updatung tabke_________________________________________-")
		rowPos = self.tableWidget.rowCount()
		self.tableWidget.insertRow(rowPos)
		# self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
		itemCount = 0
		for item in row:
			self.tableWidget.setItem(rowPos,itemCount, QTableWidgetItem(str(row[itemCount])))
			# self.tableWidget.setItem(rowPos,itemCount, QTableWidgetItem("test"))
			print(f"inserted into table ------------{row[itemCount]}-------------")
			itemCount+=1

def main():
	app = QApplication(sys.argv)
	window = UI()
	window.show()
	

	sys.exit(app.exec_())


main()