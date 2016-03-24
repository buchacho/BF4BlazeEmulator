import threading
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol
import struct, socket

import Utils.Globals as Globals
import Utils.BlazeFuncs as BlazeFuncs

class GOSRedirector(Protocol):
	def dataReceived(self, data):
		data_e = data.encode('Hex')
		packet = BlazeFuncs.BlazeDecoder(data.encode('Hex'))
		
		## REDIRECTORCOMPONENT
		if packet.packetComponent == '0005' and packet.packetCommand == '0001':
			clnt = packet.getVar("CLNT")
			
			port = 10041
			if clnt == "warsaw server":
				port = 10071
			
			#ip = ''.join([ bin(int(x))[2:].rjust(8,'0') for x in Globals.serverIP.split('.')])
			ip = struct.unpack("!I", socket.inet_aton(Globals.serverIP))[0]
			
			reply = BlazeFuncs.BlazePacket("0005","0001",packet.packetID,"1000")
			reply.writeSUnion("ADDR")
			reply.writeSStruct("VALU")
			reply.writeString("HOST", Globals.serverIP)
			reply.writeInt("IP  ", ip)
			
			reply.writeInt("PORT", port)
			reply.writeEUnion()
			reply.writeInt("SECU", 0)
			reply.writeInt("XDNS", 0)
			self.transport.write(reply.build().decode('Hex'))