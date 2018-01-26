
from scapy.all import *
from daemon import Daemon
import sys, csv, time, datetime

class DNSDaemon(Daemon):
	def run(self):
		global dns_main
		global dns_sub
		global csv_file
		global csv_write
		global domain
		global cycle
		global auto_inc
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

if __name__ == "__main__":
	daemon = DNSDaemon('/tmp/dns-daemon.pid')

	if len(sys.argv) == 2 and 'stop' == sys.argv[1]:
		daemon.stop()
		sys.exit(0)

	if len(sys.argv) == 7:
		dns_main = sys.argv[2]
		dns_sub = sys.argv[3]
		domain = sys.argv[4]
		cycle = int(sys.argv[5])
		csv_path = sys.argv[6]
		auto_inc = 1

		try:		# read existing file's last row number
			with open(csv_path, 'r') as f:
				for row in reversed(list(csv.reader(f))):
					auto_inc = int(row[0]) + 1
					break
		except:
			pass

		csv_file = open(csv_path, 'a')
		csv_write = csv.writer(csv_file)
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart [Main DNS] [Sub DNS] [Domain] [Cycle] [Path CSV File]" % sys.argv[0]
		sys.exit(2)
