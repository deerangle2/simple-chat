import socket
import bytepacker
import threading

packetPrefixes = {
	"authRequest": 0xE0,
	"authAccept": 0xE1,
	"sendMessage": 0xE2,
	"recvMessage": 0xE3
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 7529))
sock.listen(1)

clients = []
				
class ReceiveThread(threading.Thread):
	def __init__(self, conn, name):
		threading.Thread.__init__(self)
		self.conn = conn
		self.name = name

	def run(self):
		global clients
		while True:
			builder = bytepacker.BytesBuilder(self.conn.recv(1024))
			if builder.readBytes(1)[0] == packetPrefixes["sendMessage"]:
				msg = builder.readString()
				print(self.name + ": " + msg)
				for client in clients:
					builder2 = bytepacker.BytesBuilder()
					builder2.writeBytes(bytes([packetPrefixes["recvMessage"]]))
					builder2.writeString(msg)
					builder2.writeString(self.name)
					client.send(builder2.getBytes())


class AuthThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global clients

		while True:
			conn, addr = sock.accept()
			builder = bytepacker.BytesBuilder(conn.recv(1024))
			if builder.readBytes(1)[0] == packetPrefixes["authRequest"]:
				name = builder.readString()
				builder2 = bytepacker.BytesBuilder()
				builder2.writeBytes(bytes([packetPrefixes["authAccept"]]))
				conn.send(builder2.getBytes())
				print("{} logged in.".format(name))
				clients.append(conn)
				recv = ReceiveThread(conn, name)
				recv.start()


auth = AuthThread()
auth.start()

"""conn, addr = sock.accept()
builder = bytepacker.BytesBuilder(conn.recv(1024))
if builder.readBytes(1)[0] == packetPrefixes["authRequest"]:
	name = builder.readString()
	builder2 = bytepacker.BytesBuilder()
	builder2.writeBytes(bytes([packetPrefixes["authAccept"]]))
	conn.send(builder2.getBytes())
	print("{} logged in.".format(name))
	connectedClients[addr] = (name, conn)"""

"""while True:
	builder = bytepacker.BytesBuilder(conn.recv(1024))
	if builder.readBytes(1)[0] == packetPrefixes["sendMessage"]:
		msg = builder.readString()
		sender = connectedClients[addr][0]
		print(sender + ": " + msg)
		builder2 = bytepacker.BytesBuilder()
		builder2.writeBytes(bytes([packetPrefixes["recvMessage"]]))
		builder2.writeString(msg)
		builder2.writeString(sender)
		conn.send(builder2.getBytes())"""