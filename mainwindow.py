import PyQt4
from PyQt4.QtGui import *
from PyQt4 import uic
from scapy.all import *
import sys, csv, time, datetime
from daemon import Daemon

class DNSDaemon(Daemon):
	def run(self):
		global auto_inc
		global dns_main
		global dns_sub
		global g_domain
		global g_cycle
		global csv_write
		global csv_file
		while True:
			answer = sr1(IP(dst=dns_main)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=domain)),verbose=0,timeout=1)
			if not answer:
				answer = sr1(IP(dst=dns_sub)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=domain)),verbose=0,timeout=2)
				csv_write.writerow([auto_inc, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), domain, answer[DNS][DNSRR].rdata, dns_sub])
				csv_file.flush()
			else:
				csv_write.writerow([auto_inc, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), domain, answer[DNS][DNSRR].rdata, dns_main])
				csv_file.flush()
			auto_inc += 1
			time.sleep(cycle)

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
		dns_main = mainDns

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
		dns_sub = subDns

		domain = self.lineDomain.text()
		if not domain:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Fill the Domain Information")
			error_dialog.exec_()
			return
		g_domain = domain

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
		g_cycle = cycle

		csv_path = self.lineCSV.text()
		if not csv_path:
			error_dialog = QErrorMessage()
			error_dialog.showMessage("Fill the csv file path")
			error_dialog.exec_()
			return
		csv_file = open(csv_path, 'w')
		csv_write = csv.writer(csv_file)

		daemon.start()

	def btn_stop(self):
		daemon.stop()

	def btn_restart(self):
		daemon.restart()

if __name__ == "__main__":
	daemon = DNSDaemon('/tmp/dns-daemon.pid')
	auto_inc = 1
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
