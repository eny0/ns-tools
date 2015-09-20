# retrieves local logs
#
# different logs to check:
#
#		/home/*/.bash_history
#		/home/*/.nano_history
#		/var/log/messages
# 	/var/log/boot
#   /var/log/debug
#		/var/log/auth.log
#		/var/log/daemon.log
# 	/var/log/dmesg
#		/var/log/dpkg.log
#		/var/log/faillog
#		/var/log/kern.log
#		/var/log/lpr.log
#		/var/log/mail.*
#		/var/log/mysql.*
#		/var/log/user.log
#		/var/log/xorg.0.log
#		/var/log/apache2/*
#		/var/log/lighttpd/*
#		/var/log/fsck/*
#		/var/log/apport.log

import optparse

def fileExists(path):
	import os
	return os.path.exists(path)

def fileFetch(path):
	pass

def scanDir(path):
	import os

	if os.path.isdir(path):	
		print "path exists"
		import subprocess
		import shlex	

		args = shlex.split('ls -l '+path)
		list = subprocess.check_output(args)
		return list
	else:
		return False

def main():
	lc_version = "v0.01"
	logfiles = ["/var/log/messages","/var/log/boot","/var/log/debug",
		"/var/log/auth.log","/var/log/daemon.log","/var/log/dmesg"]

	parser = optparse.OptionParser("usage: log-catcher.py -o <output>")
	parser.add_option('-o', dest='oput', type='string', help='specify output file')
	(options, args) = parser.parse_args()
	if (options.oput == None):
		lc_outputfile = "log-catcher.results"
	else:
		lc_outputfile = options.oput

	print "Log Catcher "+lc_version
	print ""
	print "using outputfile: "+lc_outputfile
	print "Starting..."
	for file in logfiles:	
		print "Trying " + file
		if (fileExists(file)):
			print "success"
		else:
			print "failure"

	if scanDir('/home/myrmidex') != False:
		print scanDir('/home/myrmidex')
	else:
		print "Scan failed."


if __name__ == "__main__":
	main()
