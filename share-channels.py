#!/usr/bin/python

import xmlrpclib
import sys

SATELLITE_URL = "https://rhnsat.example.org/rpc/api"
SATELLITE_LOGIN = "admin"
SATELLITE_PASSWORD = "password"


client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

list = client.channel.listAllChannels(key)

for chan in list:

	client.channel.access.setOrgSharing(key, chan.get('label'), "public")

client.auth.logout(key)
