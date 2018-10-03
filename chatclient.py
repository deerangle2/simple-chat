import socket
import time
import threading
import sys
import bytepacker

packetPrefixes = {
	"authRequest": 0xE0,
	"authAccept": 0xE1,
	"sendMessage": 0xE2,
	"recvMessage": 0xE3
}

def connect(sock, addr, timeout):
	startTime = time.time()
	while True:
		try:
			if time.time() - startTime > timeout:
				return False
			sock.connect(addr)
		except ConnectionRefusedError:
			continue
		break
	return True

user = input("Enter username: ")

#connect and request authentication
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if connect(clientSocket, ("127.0.0.1", 7529), 5):
	builder = bytepacker.BytesBuilder()
	builder.writeBytes(bytes([packetPrefixes["authRequest"]]))
	builder.writeString(user)
	clientSocket.send(builder.getBytes())
else:
	print("Cannot reach server.")
	quit()

#authentication response
data = clientSocket.recv(1024)
if data:
	builder = bytepacker.BytesBuilder(data)
	if builder.readBytes(1)[0] == packetPrefixes["authAccept"]:
		print("Logged in as {}.".format(user))
	else:
		print("Unexpected authentication response.")
		quit()
else:
	print("Server did not respond.")
	quit()

class ChatThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			msg = input()
			builder = bytepacker.BytesBuilder()
			builder.writeBytes(bytes([packetPrefixes["sendMessage"]]))
			builder.writeString(msg)
			clientSocket.send(builder.getBytes())

class ReceiveThread(threading.Thread):
	def __init_(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			builder = bytepacker.BytesBuilder(clientSocket.recv(1024))
			if builder.readBytes(1)[0] == packetPrefixes["recvMessage"]:
				msg = builder.readString()
				sender = builder.readString()
				print(sender + ": " + msg)

#start sending messages and listening to server
chat = ChatThread()
chat.start()

recv = ReceiveThread()
recv.start()