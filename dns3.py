# -*- coding: utf-8 -*-
# 
# 2018.08.28 CR-PARK (yeoli128@gmail.com, crpark@gamevilcom2us.com)
#
# Custom DNS Server for Com2us Platform, Promotion Server Developers
#

import logging
import time
import json
import signal
import base64
import os
import datetime
import sys


# using opensource - dnslib, requests
currPath = os.path.dirname(os.path.realpath(__file__))

sys.path.append(currPath + './certifi-2019.3.9')
sys.path.append(currPath + './chardet-3.0.4')
sys.path.append(currPath + './dnslib-0.9.7')
sys.path.append(currPath + './idna-2.8')
sys.path.append(currPath + './requests-2.21.0')
sys.path.append(currPath + './urllib3-1.24.1')


import requests

from dnslib.server import DNSServer
from dnslib.server import BaseResolver
from dnslib.server import DNSLogger
from dnslib.server import RR
from dnslib.dns import *
from dnslib import QTYPE



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Local DNS binding
DNS_PORT = 53
DNS_SERVER_IPV4_ADDRESS = '0.0.0.0'
DNS_TTL = 300


# Default relay dns server
DNS_REAL_SERVER_IPV4_ADDRESS = '8.8.8.8'
DNS_REAL_PORT = 53
DNS_REAL_TIMEOUT = 30


# Target Address
FORWARDING_IPV4_ADDRESS = '192.168.0.201'


# DNS Resolver
class CustomDNSResolver(BaseResolver):

	isCustomDNSEnabled = True

	customDomainDictionary = {

		'mydomain.co.kr': FORWARDING_IPV4_ADDRESS,
		'mydomain.co.jp': FORWARDING_IPV4_ADDRESS,
		'mydomain.cn': FORWARDING_IPV4_ADDRESS,
		'mydomain.com': FORWARDING_IPV4_ADDRESS,

		'www.test.com': FORWARDING_IPV4_ADDRESS,
	}


	def __init__(self):
		None

	def enableCustomDNS(self, enable):
		self.isCustomDNSEnabled = enable

	def getNoDataDNSReply(self, reply):
		reply.header.rcode = RCODE.NXDOMAIN
		return reply

	def getRealIPAddressString(self, domainString):
		ipAddrString = None

		try:
			ipAddrString = socket.gethostbyname(domainString)
		except:
			None

		return ipAddrString

	def getIPAddressString(self, domainString):
		if self.isCustomDNSEnabled:
			try:
				return self.customDomainDictionary[domainString]
			except KeyError:
				None

		return None

	def isDNSClassA(self, qType):
		if qType == getattr(QTYPE, 'A'):
			return True

		return False

	def log(self, handler, logString):
		print("%s [%s:%s] %s" % (time.strftime("%Y-%m-%d %X"), handler.__class__.__name__, handler.server.resolver.__class__.__name__, logString), flush=True)

	def getOriginalDNSReply(self, request, reply, handler):
		# Relay
		if not reply.rr:
			try:
				if handler.protocol == 'udp':
					proxyDNSResponsePacket = request.send(DNS_REAL_SERVER_IPV4_ADDRESS, DNS_REAL_PORT, tcp=False, timeout=DNS_REAL_TIMEOUT)
				else:
					proxyDNSResponsePacket = request.send(DNS_REAL_SERVER_IPV4_ADDRESS, DNS_REAL_PORT, tcp=True, timeout=DNS_REAL_TIMEOUT)
				reply = DNSRecord.parse(proxyDNSResponsePacket)
			except socket.timeout:
				reply.header.rcode = getattr(RCODE, 'NXDOMAIN')

		return reply


	def resolve(self, request, handler):

		reply = request.reply()

		qType = request.q.qtype
		qTypeString = QTYPE[qType]


		# IPv4 Only
		isTypeA = self.isDNSClassA(qType)
		if False == isTypeA:
			reply = self.getOriginalDNSReply(request, reply, handler)
			if reply is None:
				return self.getNoDataDNSReply(request)


		try:
			queryDomainTuple = request.q.qname.label
			queryDomainString = b'.'.join(queryDomainTuple).decode('utf-8')
		except NameError:
			return self.getNoDataDNSReply(request)


		# Custom DNS Process
		ipAddrString = self.getIPAddressString(queryDomainString)
		if ipAddrString is not None:
			dnsResultString = "%s. %s %s %s" % (queryDomainString, DNS_TTL, 'A', ipAddrString)
			self.log(handler, "     *** [O] Resolved: " + dnsResultString)
			reply.add_answer(*RR.fromZone(dnsResultString))
		else:
			reply = self.getOriginalDNSReply(request,reply,handler)
			self.log(handler, "     *** [ ] Passed: " + queryDomainString)
			if reply is None:
				reply = self.getNoDataDNSReply(request)

		return reply


# DNS Server
class CustomDNSProxyServer:

	def __init__(self):
		None

	def printUsage(self):
		print("")
		print("*** Custom DNS Server Menu ***")
		print("     Q. Quit")
		print("     1. On  - Custom DNS")
		print("     2. Off - Custom DNS")
		print("     P. Print")
		print("")

	def runDNSProxy(self):
		resolver = CustomDNSResolver()
		logger = DNSLogger()
		server = DNSServer(resolver, port=DNS_PORT, address=DNS_SERVER_IPV4_ADDRESS, logger=logger)
		server.start_thread()

		# Usage
		self.printUsage()

		while True:
			inputOption = input("[Input Number] ").strip()

			try:
				inputOption = inputOption.strip().lower()
			except ValueError:
				inputOption = 0

			if 'q' == inputOption :
				break
			elif '1' == inputOption:
				resolver.enableCustomDNS(True)
				print("Custom DNS Server turned on.")
			elif '2' == inputOption:
				resolver.enableCustomDNS(False)
				print("Custom DNS Server turned off.")
			elif 'p' == inputOption:
				# Print Custom DNS Status
				print("     Feature #1 - Custom DNS Server turned ", end='')
				if resolver.isCustomDNSEnabled:
					print("on.")
				else:
					print("off.")
				print("")
			else:
				self.printUsage()


		server.stop()


if __name__ == "__main__":
	print("Custom DNS Server 0.32 final (python3), powered by dnslib. (by CR PARK)")
	print("For Com2us Platform, Promotion Server Developers.")

	dnsServer = CustomDNSProxyServer()
	dnsServer.runDNSProxy()


