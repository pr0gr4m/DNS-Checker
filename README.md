# DNS-Checker

[BOB6]DF12_Tech_06_박강민

* mainwindow.py : GUI
* dns_daemon.py : Daemon Process for checking DNS
* daemon.py : Class for Daemonizing

Environment
============

* OS : Ubuntu 16.04.3 64-bit
* Kernel : 4.13.0-26-generic
* Version : Python 2.7.12

Dependency
==========

* PyQt4, scapy

```
$ sudo apt install python python-dev build-essential python-pip
$ sudo pip install --upgrade pip
$ sudo pip install scapy
$ sudo apt install python-qt4
```

Usage
======

* Main DNS Server : Main DNS server address to send query
* Sub DNS Server : Sub DNS server address to send query
* Domain : Target domain to acquisition information(IP Address)
* Cycle : Period of reiteration
* CSV Path : Name (Path) to save CSV file
* Start : Start dns daemon process
* Stop : Stop dns daemon process
* Restart : Restart dns daemon process
