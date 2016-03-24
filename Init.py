#! python2.7
import sys
sys.dont_write_bytecode = True

import BlazeMain_Client
import BlazeMain_Server
import GosRedirector
import Https
import MySQLdb
import sys

from Utils import garbage
import Utils.Globals as Globals

from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.web import server, resource

def Start():
	Globals.serverIP = "192.168.1.40"
	
	#MySQL Data
	Globals.dbHost = "127.0.0.1"
	Globals.dbUser = "user"
	Globals.dbPass = "pass"
	Globals.dbDatabase = "db"
	
	CheckMySqlConn()
	
	SSLInfo = ssl.DefaultOpenSSLContextFactory('crt/privkey.pem', 'crt/cacert.pem')
	
	factory = Factory()
	factory.protocol = GosRedirector.GOSRedirector
	reactor.listenSSL(42127, factory, SSLInfo)
	print("[SSL REACTOR] GOSREDIRECTOR STARTED [42127]")
	
	factory = Factory()
	factory.protocol = BlazeMain_Client.BLAZEHUB
	reactor.listenTCP(10041, factory)
	print("[TCP REACTOR] BLAZE CLIENT [10041]")
	
	factory = Factory()
	factory.protocol = BlazeMain_Server.BLAZEHUB
	reactor.listenTCP(10071, factory)
	print("[TCP REACTOR] BLAZE SERVER [10071]")
	
	sites = server.Site(Https.Simple())
	reactor.listenSSL(443, sites, SSLInfo)
	print("[WEB REACTOR] Https [443]")

	reactor.run()
	
def CheckMySqlConn():
	print("[MySQL] Checking server connection...")
	
	try:
		db = MySQLdb.connect(Globals.dbHost, Globals.dbUser, Globals.dbPass, Globals.dbDatabase)
		cursor = db.cursor()        
		cursor.execute("SELECT VERSION()")
		results = cursor.fetchone()

		print("[MySQL] Server connection ok!")

			
	except MySQLdb.Error, e:
		print "[MySQL] Server connection failed! Error: %d in connection: %s" % (e.args[0], e.args[1])
		sys.exit()

	
if __name__ == '__main__':
	Start()
