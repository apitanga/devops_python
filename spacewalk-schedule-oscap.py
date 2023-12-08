#!/usr/bin/python
#
#  usage: spacewalk-schedule-oscap.py [options]
#
#  options:
#    -h, --help            show this help message and exit
#    -f CFG_FILE, --config-file=CFG_FILE
#                          Config file for servers, users, passwords
#    -p PROFILE, --profile=PROFILE
#                          Security profile name, ex: RHEL6-Default
#    -s SYSTEM, --system=SYSTEM
#                          Name of the System or "all" for all systems. Regex can
#                          be used to specify more than one server, ex.
#                          webserver*
#    -x PATH, --xccdf-path=PATH
#                          Full path to the XML format defining the security checklist.
#                          This file shoud be located on the system being scanned
#  
#
# Example configuration file: 
#
# [Spacewalk]
# server = example.com
# user   = admin
# password   = password


import xmlrpclib
import ConfigParser
import optparse
import sys
import os
import re

from optparse import OptionParser
from distutils.version import LooseVersion

def parse_args():
    parser = OptionParser()
    parser.add_option("-f", "--config-file", type="string", dest="cfg_file",
            help="Config file for servers, users, passwords")
    parser.add_option("-p", "--profile", type="string", dest="profile",
            help="Profile name, ex: RHEL6-Default")
    parser.add_option("-s", "--system", type="string", dest="system",
            help="Name of the System or \"all\" for all systems. Regex can be "
            "used to specify more than one server, ex. webserver*")
    parser.add_option("-x", "--xccdf-path", type="string", dest="path",
            help="Path to XCCDF file on client system")

    (options,args) = parser.parse_args()
    return options

def schedule_scan(spacewalk, spacekey, system, path, profile):
	profile = "--profile %s" % profile
	spacewalk.system.scap.scheduleXccdfScan(spacekey, system["id"], path, profile)
	print system
	print path
	print profile

def main():         
    # Get the options
    options = parse_args()
    # read the config
    if options.cfg_file: 
        config = ConfigParser.ConfigParser()
        try:
            config.read (options.cfg_file) 
        except:
            print "Could not read config file %s.  Try -h for help" % options.cfg_file
            sys.exit(1)
        try: 
            server = config.get ('Satellite', 'server')
            user = config.get ('Satellite', 'user')
            password = config.get ('Satellite', 'password')
        except: 
            print "The file %s seems not to be a valid config file." % options.cfg_file
            sys.exit(1)
    else:
        print "Options -f (Configfile) not given! Try -h for help"
        sys.exit(1)

    if options.system is None or options.profile is None or options.path is None:
        print "Missing XCCDF path, SCAP profile or system name.  Try -h for help"
        sys.exit(1)

    spacewalk = xmlrpclib.Server("https://%s/rpc/api" % server, verbose=0)
    spacekey = spacewalk.auth.login(user,password)

        
  
    if options.system == "all":
        entries=spacewalk.system.listSystems(spacekey)
    else:
        entries=spacewalk.system.searchByName(spacekey, options.system)
    if entries:
        for entry in entries:
            #print entry["id"]
		schedule_scan(spacewalk, spacekey, entry, options.path, options.profile)

    else:
        print "No system(s) found" % options.system
        spacewalk.auth.logout(spacekey)
        sys.exit(1)
    spacewalk.auth.logout(spacekey)

## MAIN
if __name__ == "__main__":
    main()  
