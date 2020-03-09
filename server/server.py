#!/usr/bin/env python3

import socket
import select
import os
import time
import logging


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
		config_params["listen_backlog"] = int(os.environ["SERVER_LISTEN_BACKLOG"])
	except KeyError as e:
		raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
	except ValueError as e:
		raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

	return config_params

def main():
	initialize_log()
	config_params = parse_config_params()
	server_sock = initialize_server_socket(
		config_params["port"],
		config_params["listen_backlog"],
	)
	start_server_loop(server_sock)

def initialize_log():
	"""
	Python custom logging initialization
	
	Current timestamp is added to be able to identify in docker
	compose logs the date when the log has arrived
	"""
	logging.basicConfig(
		format='%(asctime)s %(levelname)-8s %(message)s',
		level=logging.INFO,
		datefmt='%Y-%m-%d %H:%M:%S',
	)

def initialize_server_socket(port, backlog):
	"""
	Initialize server socket 

	Server socket is initialized as a TCP stream socket.
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', port))
	s.listen(backlog)
	return s

def accept_new_connection(server_sock):
	"""
	Accept new connections

	Client sockets created from the connection are set as
	nonblocking sockets to be added into the select syscall
	to listen to messages to be received
	"""
	# Connection arrived
	logging.info("Proceed to accept new connections")
	c, addr = server_sock.accept()

	# Sockets received by select syscall must be non blocking.
	c.setblocking(0)

	# Append the socket to the select input list to detect when
	# traffic arrives from a client
	logging.info('Got connection from {}'.format(addr)) 
	return c

def handle_client_connection(client_sock):
	"""
	Read message from a specific client socket

	If client socket is closed, return false
	"""
	try:
		msg = client_sock.recv(1024)
		logging.info(
			'Message received from connection {}. Msg: {}'
				.format(client_sock.getpeername(), msg))
		client_sock.send(b"Your Message has been received.\n")
	except OSError:
		logging.info("Client socket {} is closed.".format(client_sock))
		client_sock.close()
		return True
	return False

def start_server_loop(server_sock):
	"""
	Server loop based on select syscall

	Select syscall is used to listen in the server socket. When a 
	connection is accepted, the socket created to communicate with
	the client will be added into the select readable list to be 
	able to listen to both new connections and client messages in the
	same thread
	"""

	# Sockets received by select syscall must be non blocking.
	server_sock.setblocking(0)
	inputs = [server_sock]
 
	while inputs:
		# TODO: Select blocks until one of the sockets receives an event. 
		# Add timeouts to handle server gracefuly quit scenario 
		# (signal handling)
		readable, _, _ = select.select(inputs, [], inputs)
		for s in readable:
			if s is server_sock:
				c = accept_new_connection(s)
				inputs.append(c)
			else:
				if handle_client_connection(s):
					inputs.remove(s)

if __name__== "__main__":
	main()
