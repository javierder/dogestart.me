# -*- coding: utf8 -*-


import sys
sys.path.append("/twitter")
from twitter import *


OAUTH_TOKEN = ""
OAUTH_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = "" 
# see "Authentication" section below for tokens and keys
t = Twitter(
            auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET)
           )





##sys.path.append("/Users/javyer/code/dogestartme/")
#sys.path.append("/home/tribalo/dogestart/")#code/dogestartme/")
sys.path.append("/home/tribalo/dogestart/")

#from dogestartme import settings
#from django.core.management import setup_environ
#setup_environ(settings)

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dogestartme.settings")
from django.conf import settings


import dogecoinrpc
import sys, time
from core.models import Bounty

serverIP = '127.0.0.1'
serverPort = '44555'
user = 'dogecoinrpc'
password = ''
# address = 'AddressToSendCoinTo'
serverIP = '127.0.0.1'
serverPort = '22555'#44555'
user = 'dogecoinrpc'
password = ''#'

fee = 0.001



conn = dogecoinrpc.connect_to_remote(user, password, host=serverIP, port=serverPort)

for b in Bounty.objects.filter(funded=False):
	if b.address != "":
		# print b.address
		# print conn.getreceivedbyaddress(b.address)
		#print conn.getreceivedbyaddress(b.address)
		#print b.amount
		#print "--"
		#print conn.getreceivedbyaddress(b.address) == b.amount
		if float(conn.getreceivedbyaddress(b.address)) >= b.amount:
			print "Bounty %s got funded with %d" % (b.title, b.amount)
			b.funded = True
			b.save()
			burl = " #dogecoin http://dogestart.me/bounties/view/" + str(b.pk) 
			
			if len(b.title) > 95 :
				btit =  b.title[0:99] + "..."
			else:
				btit = b.title

			btit = btit + " (%d doge)" % b.amount

			t.statuses.update(status="%s%s" %(btit,burl))


		# else:
		# 	print b.title
		# 	print conn.getreceivedbyaddress(b.address)
