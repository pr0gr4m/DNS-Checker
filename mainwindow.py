import PyQt4
from PyQt4.QtGui import *
from PyQt4 import uic
import time, sys, csv
import os, subprocess

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
		self.btnRestart.clicked.connect(self.btn_restart)

	def btn_csv(self):
		csv_path = QFileDialog.getSaveFileName(self, "Save CSV File", "", ".csv") + ".csv"
		self.lineCSV.setText(csv_path)

	def get_config(self):
		global mainDns
		global subDns
		global domain
		global cycle
		global csv_path

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

		domain = self.lineDomain.text()
		if not domain:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Fill the Domain Information")
			error_dialog.exec_()
			return

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

		csv_path = self.lineCSV.text()
		if not csv_path:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Fill the csv file path")
			error_dialog.exec_()
			return

	def btn_start(self):
		global mainDns
		global subDns
		global domain
		global cycle
		global csv_path
		self.startFlag = True
		self.get_config()
		subprocess.call(["python", "dns_daemon.py", "start", mainDns, subDns, domain, str(cycle), csv_path])

	def btn_stop(self):
		self.startFlag = False
		subprocess.call(["python", "dns_daemon.py", "stop"])

	def btn_restart(self):
		global mainDns
		global subDns
		global domain
		global cycle
		global csv_path
		self.get_config()
		subprocess.call(["python", "dns_daemon.py", "restart", mainDns, subDns, domain, str(cycle), csv_path])

if __name__ == "__main__":
	mainDns = ""
	subDns = ""
	domain = ""
	cycle = 3600
	csv_path = ""
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
