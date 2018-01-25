from PyQt4.QtGui import *
from PyQt4 import uic
import sys

form_class = uic.loadUiType("dns.ui")[0]

class MainWindow(QMainWindow, form_class):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
	
		self.btnCSV.clicked.connect(self.btn_csv)
		self.btnStart.clicked.connect(self.btn_start)
		self.btnStop.clicked.connect(self.btn_stop)
		self.btnDetail.clicked.connect(self.btn_detail)

	def btn_csv(self):
		self.lineCSV.setText("ok")

	def btn_start(self):
		mainDns = ""
		if self.dnsGoogleMain.isChecked():
			mainDns = self.dnsGoogleMain.text()
		elif self.dnsQuadMain.isChecked():
			mainDns = self.dnsQuadMain.text()
		elif self.dnsFreeMain.isChecked():
			mainDns = self.dnsFreeMain.text()
		else:
			mainDns = self.dnsLevelMain.text()
		print mainDns

		subDns = ""
		if self.dnsGoogleSub.isChecked():
			subDns = self.dnsGoogleSub.text()
		elif self.dnsQuadSub.isChecked():
			subDns = self.dnsQuadSub.text()
		elif self.dnsFreeSub.isChecked():
			subDns = self.dnsFreeSub.text()
		else:
			subDns = self.dnsLevelSub.text()
		print subDns

		cycle = 3600
		if self.cycleHour.isChecked():
			cycle = 3600
		elif self.cycleMinute.isChecked():
			cycle = 60
		else:
			cycle = 1
		print cycle

	def btn_stop(self):
		print "tmp"

	def btn_detail(self):
		print "tmp"

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
