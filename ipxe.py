#!/usr/bin/python

###############################
########## LIBRARIES ##########

# Library used to connect to cobbler's API
import xmlrpclib
# Library used to get URL variables
import cgi
# Library providing generic python commands
import sys
# Library providing access to the underlying RHEL server
import os

################################
######## FUNCTIONS #############

def print_menu(): # This function tells iPXE to boot to the default cobbler menu
	print "#!ipxe"
	print "set 209:string pxelinux.cfg/default"
	print "set 210:string http://%s/pub/tftpboot/" % boot_server
	print "boot http://%s/pub/tftpboot/pxelinux.0" % boot_server

def boot_system(): # while this one tells it to boot a system directly instead
	print "#!ipxe"
	print "set mirror http://%s" % boot_server
	print "set repo ${mirror}%s" % media_path
	# Boot new system and provision it using the kernel image and initrd disk provided by the specific distro and the kickstart file defined for the specific system
	print "kernel ${repo}/images/pxeboot/vmlinuz ksdevice=bootif lang=  kssendmac text ks=${mirror}/cblr/svc/op/ks/system/%s" % (system)
	print "initrd ${repo}/images/pxeboot/initrd.img"
	print "boot"

def define_mediatype(): # We need to define what type of file we're serving
	print "Content-Type: text/plain"
	print ""
 
def boot_disk(): # This one will tell iPXE to boot to local disk (HD)
        print "#!ipxe"
        print "sanboot --no-describe --drive 0x80 || exit"


##################################
######### VARIABLES ##############

# We default to not booting a system unless it's permitted explicitly
netboot_enabled = False

# We assume the system is unknown unless we explicitly find it in cobbler
system = 'Unknown'

# Get client's IP address
client_IP = os.environ["REMOTE_ADDR"]
# Define appropriate source of bits depending on origin subnet 
if '10.128.' in client_IP:
	boot_server = 'wfcvsatproxypr01.example.com'
elif '10.125.' in client_IP:
	boot_server = 'nybvsatproxypr01.example.com'
elif '10.135.'in client_IP:
	boot_server = 'lncvsatproxypr01.example.com'
elif '10.137.' in client_IP:
	boot_server = 'lncvsatproxypr01.example.com'
elif '10.126.246.' in client_IP:
	boot_server = 'nylvsatproxypr01.example.com'
else:
	boot_server = 'njcvsatpr01.example.com'

# Retrieve variables sent from iPXE ISO
ipxe_vars = cgi.FieldStorage()

# This is the MAC address by which the system should be know to cobbler (i.e. during 'cobbler system add')
ipxe_mac = ipxe_vars["mac"].value

#################################
##########ACTION#################

# Connect to cobbler's API
server = xmlrpclib.Server("http://127.0.0.1/cobbler_api")

# Check if system is indeed known to cobbler
if server.find_system({"mac_address":ipxe_mac}):
# if so then let's use this system's information for the build
	system = server.find_system({"mac_address":ipxe_mac})
# Grab system's name
	system = system[0]
# Get information about this particular cobbler system
	system_info = server.get_system(system)
	netboot_enabled = system_info['netboot_enabled']
# Get system's profile name
	kickstart_profile = system_info['profile']
# Get information about the profile this system inherits
	kickstart_profile_info = server.get_profile(kickstart_profile)
# Get distro's name
	distro = kickstart_profile_info['distro']
# Get information about the distro this profile inherits
	distro_info = server.get_distro(distro)
# Get distro's kickstart metadata, where media path is defined
	ks_meta = distro_info['ks_meta']
# Get distro's media path
	media_path = ks_meta['media_path']

define_mediatype() # Print appropriate iPXE boot script

if system is 'Unknown':
        print_menu() # If the system is unknown (new guy) present build menu
else: # If the system is known to cobbler
        if netboot_enabled == True:
                boot_system()
        else: # If the system is known but doesn't have netboot enabled
                boot_disk()
sys.exit()
