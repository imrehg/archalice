#!/usr/bin/env python

import os
import re
import time
import sys
import fileinput
from threading import Thread

class testhost(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
        self.responsetime = -1

    def run(self):
        pingaling = os.popen("ping -q -c2 "+self.ip+" 2>&1","r")
        while 1:
            line = pingaling.readline()
            if not line: break
            igot = re.findall(self.lifeline,line)
            if igot:
                self.status = int(igot[0])
                line = pingaling.readline()
                # Use only the first occurence, that is average response
                restime = re.search(self.response, line)
                if  restime:
                    self.responsetime = restime.group(1)

testhost.lifeline = re.compile(r"(\d) received")
# Fit a floating point value, to get average latency from this kind of line:
# rtt min/avg/max/mdev = 0.883/0.902/0.921/0.019 ms
testhost.response = re.compile(r'/((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)/')
report = ("No response","Partial Response","Alive")

print time.ctime()

pinglist = []
hostlist = dict({})

# Load host list from "mirrorlist"
mirrorlist = "/etc/pacman.d/mirrorlist"
for line in fileinput.input(mirrorlist):
    host = re.search(r'(http|ftp)://(.*?)/', line)
    if host:
        hostlist[host.group(2)] = -1

for list in hostlist.iterkeys():
    current = testhost(list)
    pinglist.append(current)
    current.start()

for pingle in pinglist:
    pingle.join()
    if (pingle.status == 2):
        hostlist[pingle.ip] = pingle.responsetime
#    print "Status from ",pingle.ip,"is",report[pingle.status],"time:",pingle.responsetime

alist = sorted(hostlist.iteritems(), key=lambda (k,v): (v,k))
for i in range(0,len(alist)):
    if (hostlist[alist[i][0]] > 0):
        print alist[i][0],":",hostlist[alist[i][0]]

print time.ctime()
