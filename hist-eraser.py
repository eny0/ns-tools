#!/usr/bin/python
# History Eraser v0.01

# Erases traces on a foreign pc

# Arguments
#
# -u : Specify the user to wipe
# -b : Use backed up files // will be implemented after Hist-Saver is complete.
# -h : Show help

# Could be used in conjunction with a 'History Saver' that backs up the old logs and this
# eraser could then restore those old log files back after erasing the new ones

def main():
	import optparse

	he_version = "v0.01"

	parser = optparse.OptionParser("Usage: hist-eraser.py -u <user>")
	parser.add_option('-u', '--user', dest='username', type='string', help='Specify user using -u')
	(options, args) = parser.parse_args()
	if options.username == None:
		print "Specify User by using -u <username>"
		exit(0)
	he_user = options.username
	print "Appointed User: "+he_user

	user_files = [".bash_history"]
	if he_user == "root":	
		user_dir = "/root/"
	else:
		user_dir = "/home/"+he_user+"/"

	# let's do history first, get that out of the way
	# history -c
	import shlex
	import subprocess
	print "Erasing terminal history... ",
	try:
#		subprocess.check_output('history -c', shell=True)
		subprocess.call(['bash','-c', 'history -c'])
		print "[OK]"
	except:
		print "[FAIL]"	

	# > /home/user/.bash_history

	import os
	
	print "Erasing .bash_history of user " + he_user+"... ",

	if not os.path.isdir(user_dir):
		print "[FAIL]"
		print user_dir+" doesnt exist - nothing for me to erase"
	else:
		if not os.path.exists(user_dir + ".bash_history"):
			print "[FAIL]"
			print user_dir+".bash_history - path does not exist"
		else:
			try:				
				list = subprocess.check_output("> "+user_dir+".bash_history", shell=True)
				print "[OK]"
			except Exception, e:
				print "[FAIL]"
				print "Error: "+str(e)

if __name__ == "__main__":
	main()
