#!/usr/bin/env python
import os
import sys
import subprocess

if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s TIMMING\n" % (sys.argv[0]))
    sys.exit(1)

timming=sys.argv[1]
command = "cat /p/lscratchf/do7/log/* | grep " + timming + " > /p/lscratchf/do7/log/" + timming + ".log"
os.system(command)

ps = subprocess.Popen(["cat", "/p/lscratchf/do7/log/" + timming + ".log"], stdout=subprocess.PIPE)
lines = subprocess.check_output(["wc","-l"],stdin=ps.stdout)

if int(lines) > 0: 
	with open("/p/lscratchf/do7/log/" + timming + ".log") as log_file:
		n = 0
		t = 0
		for line in log_file:
			l = line.split("=")
			t += float(l[1])
			n += 1
		print(timming + "_write= %s" % str(t/n))
