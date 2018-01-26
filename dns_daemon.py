
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
	dns_main = "8.8.8.8"
	dns_sub = "8.8.4.4"
	csv_file = open('data.csv', 'w')
	csv_write = csv.writer(csv_file)
	domain = "fl0ckfl0ck.info"
	cycle = 2
	auto_inc = 1
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
