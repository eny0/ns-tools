#!/usr/bin/python
# local-enum v0.01
#
#	Enumerates all important files on a device.

outbuf = ""

def runCmds(commands):
	outbuffer = ""
	for cmd in commands:
		import shlex
		import subprocess
		args = shlex.split(cmd)
		try:
			outp = subprocess.check_output(args)
			outbuffer += "# "+cmd+"\n"
			outbuffer += outp
			outbuffer += "\n"
		except:
			pass
	writeBuf(outbuffer)

def writeBuf(msg):
	global outbuf
	outbuf += msg+"\n"

def writeOut(file):
	global outbuf
	if file == None:
		print outbuf
	else:
		import os
		print "Results saved in "+str(file)
		if not os.path.exists(file):
			import shlex, subprocess
			args = shlex.split("touch "+file)
			subprocess.check_output(args)
		f = open(file, 'r+')
		f.write(outbuf)
		f.close()	

def checkExists(file):
	import os
	if os.path.exists(file):
		return True
	else:
		return False

def main():
	import optparse
	
	parser = optparse.OptionParser("usage: local-enum.py -o <output>")
	parser.add_option('-o', dest='outputfile', type='string', help='specify output file')
	(options, args) = parser.parse_args()
	le_outputfile = options.outputfile
	le_version = "v0.01"

	#kernel commands
	writeBuf("# KERNEL COMMANDS\n")
	commands = ["uname -a","uname -r","uname -n","hostname","uname -m"]
	catpaths = ["/proc/version","/etc/*-release","/etc/issue"]
	for cp in catpaths:
		if checkExists(cp):
			commands.append("cat "+cp)
	runCmds(commands)

	#users & groups
	writeBuf("\n# USERS & GROUPS\n")
	commands = ["finger","pinky","users","who -a","w","last","lastlog"]
	catpaths = ["/etc/passwd","/etc/group","/etc/shadow"]
	for cp in catpaths:
		if checkExists(cp):
			commands.append("cat "+cp)
	runCmds(commands)

	# User & Privilege info
	writeBuf("\n# USER & PRIV INFO\n")
	commands = ["whoami","id","sudo -l"]
	catpaths = ["/etc/sudoers"]
	for cp in catpaths:
		if checkExists(cp):
			commands.append("cat "+cp)
	runCmds(commands)

	# Environmental Info
	writeBuf("\n# ENVIRONMENTAL INFORMATION\n")
	commands = ["env","set","echo $PATH","history","pwd"]
	catpaths = ["/etc/profile","/etc/shells"]
	for cp in catpaths:
		if checkExists(cp):
			commands.append("cat "+cp)
	runCmds(commands)

	# Interesting Files
	writeBuf("\n# INTERESTING FILES\n")
	commands = ["find / -perm -4000 -type f 2>/dev/null"]
	runCmds(commands)
	# needs more ...

	# Service Info
	writeBuf("\n# SERVICE INFO\n")
	commands = ["ps -aux | grep root"]
	catpaths = ["/etc/inetd.conf","/etc/xinetd.conf"]
	for cp in catpaths:
		if checkExists(cp):
			commands.append("cat "+cp)
	runCmds(commands)

	# Jobs/Tasks
	writeBuf("\n# JOBS/TASKS\n")
	commands = ["crontab -l", "top"]
#	runCmds(commands)

	# Networking, Routing & Communications
	writeBuf("\n# NETWORKING, ROUTING & COMMUNICATIONS\n")
	commands = ["/sbin/ifconfig -a","arp -a","route","netstat -antp",
		"netstat -anup","iptables -L"]
	catpaths = ["/etc/network/interfaces","/etc/resolv.conf","/etc/services"]
	for cp in catpaths:
		if checkExists(cp):
			commands.append("cat "+cp)
	runCmds(commands)

	# Programs Installed
	writeBuf("\n# PROGRAMS INSTALLED\n")
	commands = ["dpkg -l","rpm -qa","sudo -V","httpd -v","apache2 -v",
		"apache2ctl -M","mysql --version","psql -V","perl -v","java -version",
		"python --version","ruby -v"]
	runCmds(commands)	


	writeOut(le_outputfile)	

if (__name__ == "__main__"):
	main()
