#!/usr/bin/env python

import os
import re
import time
import sys
from threading import Thread

class testhost(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
        self.responsetime = -1

    def run(self):
        pingaling = os.popen("ping -q -c2 "+self.ip,"r")
        while 1:
            line = pingaling.readline()
            if not line: break
            igot = re.findall(self.lifeline,line)
            if igot:
                self.status = int(igot[0])
                line = pingaling.readline()
                restime = re.search(self.response, line)
                if  restime:
                    self.responsetime = restime.group(1)

testhost.lifeline = re.compile(r"(\d) received")
testhost.response = re.compile(r'((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) ms')
report = ("No response","Partial Response","Alive")

print time.ctime()

pinglist = []

for host in range(1,10):
    ip = "192.168.11."+str(host)
    current = testhost(ip)
    pinglist.append(current)
    current.start()

for pingle in pinglist:
    pingle.join()
    print "Status from ",pingle.ip,"is",report[pingle.status],"time:",pingle.responsetime

print time.ctime()
