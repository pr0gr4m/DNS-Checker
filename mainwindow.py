import PyQt4
from PyQt4.QtGui import *
from PyQt4 import uic
import sys

form_class = uic.loadUiType("dns.ui")[0]

class MainWindow(QMainWindow, form_class):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.startFlag = False
		self.lineCSV.setReadOnly(True)
	
		self.btnCSV.clicked.connect(self.btn_csv)
		self.btnStart.clicked.connect(self.btn_start)
		self.btnStop.clicked.connect(self.btn_stop)
		self.btnDetail.clicked.connect(self.btn_detail)

	def btn_csv(self):
		csv_path = QFileDialog.getSaveFileName(self, "Save CSV File", "", ".csv") + ".csv"
		self.lineCSV.setText(csv_path)

	def btn_start(self):
		self.startFlag = True

		mainDns = ""
		if self.dnsGoogleMain.isChecked():
			mainDns = self.dnsGoogleMain.text()
		elif self.dnsQuadMain.isChecked():
			mainDns = self.dnsQuadMain.text()
		elif self.dnsFreeMain.isChecked():
			mainDns = self.dnsFreeMain.text()
		elif self.dnsLevelMain.isChecked():
			mainDns = self.dnsLevelMain.text()
		else:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Check Main DNS Server")
			error_dialog.exec_()
			return
		print mainDns

		subDns = ""
		if self.dnsGoogleSub.isChecked():
			subDns = self.dnsGoogleSub.text()
		elif self.dnsQuadSub.isChecked():
			subDns = self.dnsQuadSub.text()
		elif self.dnsFreeSub.isChecked():
			subDns = self.dnsFreeSub.text()
		elif self.dnsLevelSub.isChecked():
			subDns = self.dnsLevelSub.text()
		else:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Check Sub DNS Server")
			error_dialog.exec_()
			return
		print subDns

		cycle = 3600
		if self.cycleHour.isChecked():
			cycle = 3600
		elif self.cycleMinute.isChecked():
			cycle = 60
		elif self.cycleSecond.isChecked():
			cycle = 1
		else:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Check Cycle")
			error_dialog.exec_()
			return
		print cycle

	def btn_stop(self):
		print "tmp"

	def btn_detail(self):
		if self.startFlag == False:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Detail can be seen after starting")
			error_dialog.exec_()
			return
		print "tmp"

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
