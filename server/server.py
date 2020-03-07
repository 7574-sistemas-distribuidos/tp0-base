#!/usr/bin/env python3

import socket
import select
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
	config_params = parse_config_params()
	server_sock = initialize_server_socket(config_params["port"])
	start_server_loop(server_sock)

def initialize_server_socket(port):
	s = socket.socket()
	s.bind(('', port))
	s.listen(5)
	return s

def start_server_loop(server_sock):
	# Sockets received by select syscall must be non blocking.
	server_sock.setblocking(0)
	inputs = [server_sock]
	outputs = []

	# TODO: Input sockets are never returned. Define a protocol between
	# the client and the server to close client sockets after communication
	# has finished 
	while inputs:
		# TODO: Select blocks until one of the sockets receives an event. 
		# Add timeouts to handle server gracefuly quit scenario 
		# (signal handling)
		readable = select.select(inputs, outputs, inputs)

		for s in readable:
			if s is server_sock:
				# Connection arrived
				c, addr = server_sock.accept()

				# Sockets received by select syscall must be non blocking.
				c.setblocking(0)

				# Append the socket to the select input list to detect when
				# traffic arrives from a client
				inputs.append(c)
				print('Got connection from {}'.format(addr)) 
			else:
				msg = c.recv(1000)
				print('Message received from connection {}. Msg: {}', s.getpeername(), msg)
				c.send('Your Message has been received.')

if __name__== "__main__":
	main()
