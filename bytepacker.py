import math

class IntHelper:
	def _decimalToBinary(self, dec):
		if dec < 0:
			b = '{0:032b}'.format(abs(dec)-1)
			o = ""
			for c in b:
				o += ("0" if c == "1" else "1")
			return o
		else:
			return '{0:032b}'.format(dec)

	def _binaryToBytes(self, b):
		o = bytes()
		extraBits = len(b) % 8
		if extraBits > 0:
			b = "0" * (8 - extraBits) + b
		for i in range(math.ceil(len(b) / 8)):
			bytebits = b[i*8:(i+1)*8]
			o += bytes([int(bytebits, 2)])
		return o

	def int32ToBytes(self, i):
		if i >= -(2**31) and i < 2**31:
			return self._binaryToBytes(self._decimalToBinary(i))
		else:
			raise ValueError("Value must be between {} and {} (inclusive)".format(-(2**31), 2**31-1))

	def bytesToInt32(self, b):
		return int.from_bytes(b, "big", signed=True)

class BytesBuilder:
	def __init__(self, data=bytes()):
		self.data = data
		self.helper = IntHelper()
		self.read_pos = 0

	def writeInt(self, i):
		self.data += self.helper.int32ToBytes(i)

	def writeBytes(self, b):
		self.data += b

	def writeString(self, s):
		self.writeInt(len(s))
		self.writeBytes(bytes(s, "utf-8"))

	def readInt(self):
		d = self.data[self.read_pos:self.read_pos+4]
		self.read_pos += 4
		return self.helper.bytesToInt32(d)

	def readBytes(self, l):
		d = self.data[self.read_pos:self.read_pos+l]
		self.read_pos += l
		return d

	def readString(self):
		strlen = self.readInt()
		strbytes = self.readBytes(strlen)
		return strbytes.decode("utf-8")

	def getBytes(self):
		return self.data