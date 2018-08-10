#!/usr/bin/python
import ConfigParser 
from shutil import copyfile
import sys
import os.path

if not os.path.exists("MobaXterm.ini") or not os.path.exists("WinSCP.ini"):
	print "MobaXterm.ini and/or WinSCP.ini are missing. Please place them in the same directory as the script"
	sys.exit()

moba_parser = ConfigParser.ConfigParser()
print "Reading MobaXterm.ini" 
moba_parser.read('MobaXterm.ini')

winscp_parser = ConfigParser.ConfigParser()
print "Reading WinSCP.ini" 
winscp_parser.read('WinSCP.ini')

tmp_parser = ConfigParser.ConfigParser()
tmp_parser.optionxform = str                                         #keep options capitalization#


servers =[]
for section_name in moba_parser.sections():
	if "Bookmarks" in section_name:
		#print 'Section:', section_name
		#print '	 Options:', moba_parser.options(section_name)
		for name, value in moba_parser.items(section_name):
			if value.startswith("#109#"):                           #Only fetch ssh sessions - 109 "
				split1 = value.split('#')
				split2 = split1[2].split('%')
				dir = moba_parser.get(section_name, 'subrep')
				tmp = (dir.replace("\\","/")+'/'+name).replace(" ","%20")
				session = 'Sessions\\' + tmp
				if winscp_parser.has_section(session):
					print "Session already present in WinSCP.ini...Will not add session  [" + name + "]"
				else:
					print "Session not present in WinSCP.ini...Will add session [" + name + "]"
					server=[session,split2[1], split2[2],split2[3]]
					servers.append(server)

for srv in servers:
	tmp_parser.add_section(srv[0])
	tmp_parser.set(srv[0],"HostName",srv[1])
	tmp_parser.set(srv[0],"UserName", srv[3])
	tmp_parser.set(srv[0],"PortNumber", srv[2])
	tmp_parser.set(srv[0],"FSProtocol", 0)
	tmp_parser.set(srv[0],"Password", "password")   #add a dummy password so you get prompt to change it and 
		                                            #save after the first unsuccessful login in WinSCP)


copyfile('WinSCP.ini', 'WinSCP.ini.bkp')		    #backup before writing new file#

#winscp_parser.write(sys.stdout)
with open('WinSCP.ini', 'ap') as f:
	tmp_parser.write(f)