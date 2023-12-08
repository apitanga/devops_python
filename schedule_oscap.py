#!/usr/bin/python

# Import necessary libraries
import xmlrpclib
import ConfigParser
import optparse
import sys
import os
import re
from optparse import OptionParser
from distutils.version import LooseVersion

# Function to parse command-line arguments
def parse_args():
    parser = OptionParser()
    parser.add_option("-f", "--config-file", type="string", dest="cfg_file", help="Config file for servers, users, passwords")
    parser.add_option("-p", "--profile", type="string", dest="profile", help="Security profile name, ex: RHEL6-Default")
    parser.add_option("-s", "--system", type="string", dest="system", help="Name of the System or \"all\" for all systems. Regex can be used to specify more than one server, ex. webserver*")
    parser.add_option("-x", "--xccdf-path", type="string", dest="path", help="Path to XCCDF file on client system")
    (options, args) = parser.parse_args()
    return options

# Function to schedule an OpenSCAP scan on a given system
def schedule_scan(spacewalk, spacekey, system, path, profile):
    profile_arg = "--profile %s" % profile
    spacewalk.system.scap.scheduleXccdfScan(spacekey, system["id"], path, profile_arg)
    print(system)
    print(path)
    print(profile_arg)

# Main function where script execution begins
def main():         
    # Get the command-line options
    options = parse_args()

    # Read and parse the configuration file
    if options.cfg_file: 
        config = ConfigParser.ConfigParser()
        try:
            config.read(options.cfg_file) 
        except:
            print("Could not read config file %s. Try -h for help" % options.cfg_file)
            sys.exit(1)
        try: 
            server = config.get('Satellite', 'server')
            user = config.get('Satellite', 'user')
            password = config.get('Satellite', 'password')
        except: 
            print("The file %s seems not to be a valid config file." % options.cfg_file)
            sys.exit(1)
    else:
        print("Options -f (Configfile) not given! Try -h for help")
        sys.exit(1)

    # Check for missing mandatory options
    if options.system is None or options.profile is None or options.path is None:
        print("Missing XCCDF path, SCAP profile or system name. Try -h for help")
        sys.exit(1)

    # Connect to the Spacewalk server
    spacewalk = xmlrpclib.Server("https://%s/rpc/api" % server, verbose=0)
    spacekey = spacewalk.auth.login(user, password)

    # Determine which systems to schedule for scanning
    if options.system == "all":
        entries = spacewalk.system.listSystems(spacekey)
    else:
        entries = spacewalk.system.searchByName(spacekey, options.system)

    # Schedule scans for the selected systems
    if entries:
        for entry in entries:
            schedule_scan(spacewalk, spacekey, entry, options.path, options.profile)
    else:
        print("No system(s) found")
        spacewalk.auth.logout(spacekey)
        sys.exit(1)

    # Logout from the Spacewalk server
    spacewalk.auth.logout(spacekey)

# Check if the script is being run directly and, if so, call the main function
if __name__ == "__main__":
    main()
