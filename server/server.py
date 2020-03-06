#!/usr/bin/env python3

import socket
import os


def parse_config_params():
	""" Parse env variables to find program config params

	Function that search and parse program configuration parameters in the 
	program environment variables. If at least one of the config parameters
	is not found a KeyError exception is thrown. If a parameter could not 
	be parsed, a ValueError is thrown. If parsing succeeded, the function
	returns a map with the env variables
	"""
	config_params = {}
	try:
		config_params["port"] = int(os.environ["SERVER_PORT"])
	except KeyError as e:
		raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
	except ValueError as e:
		raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

	return config_params

def main():
	"""
	"""
	
	config_params = parse_config_params()
	server_sock = initialize_server_socket(config_params["port"])
	start_server_loop(server_sock)

def initialize_server_socket(port):
	s = socket.socket()
	s.bind(('', port))
	s.listen(5)
	return s

def start_server_loop(server_sock):
	while True: 
		c, addr = server_sock.accept()   
		print('Got connection from {}'.format(addr)) 
	
		while True:
			msg = c.recv(1000)
			print("Message from client: {}".format(msg))
			c.send('Your message has been received.')

if __name__== "__main__":
	main()
