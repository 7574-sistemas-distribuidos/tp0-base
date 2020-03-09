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

	Function blocks until a connection to a client is made.
	Then connection created is printed and returned
	"""

	# Connection arrived
	logging.info("Proceed to accept new connections")
	c, addr = server_sock.accept()
	logging.info('Got connection from {}'.format(addr)) 
	return c

def handle_client_connection(client_sock):
	"""
	Read message from a specific client socket and close the socket

	If a problem arises in the communication with the client, the 
	client socket will also be closed
	"""
	try:
		msg = client_sock.recv(1024)
		logging.info(
			'Message received from connection {}. Msg: {}'
				.format(client_sock.getpeername(), msg))
		client_sock.send(b"Your Message has been received.\n")
	except OSError:
		logging.info("Error while reading socket {}".format(client_sock))
	finally:
		client_sock.close()

def start_server_loop(server_sock):
	"""
	Dummy Server loop

	Server that accept a new connections and establishes a 
	communication with a client. After client with communucation
	finishes, servers starts to accept new connections again  
	"""

	# TODO: Modify this program to handle signal to graceful shutdown
	# the server
	while True:
		client_sock = accept_new_connection(server_sock)
		handle_client_connection(client_sock)

if __name__== "__main__":
	main()
