# -*- coding: utf8 -*-


import sys

sys.path.append("/home/tribalo/dogestart/")

#from django.core.management import setup_environ
#setup_environ(settings)

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dogestartme.settings")
from django.conf import settings
from django.db.models import Sum

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

data = Bounty.objects.exclude(completed=None).aggregate(Sum('amount'))
print data
total = data["amount__sum"] * 0.01
print total