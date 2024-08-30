import struct

def htonl(value):
    return struct.pack('>I', value)

def ntohl(value):
    return struct.unpack('>I', value)[0]