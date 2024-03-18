#!/bin/bash

add_compose_header() {
    echo "version: '3.9'
name: tp0
services:
" > docker-compose.yml
}

add_server() {
    echo "  
  server:
    container_name: server
    image: server:latest
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net
" >> docker-compose.yml
}

add_clients() {
    local num_clients=$1
    for ((i=1; i<=$num_clients; i++)); do
        echo "
  client$i:
    container_name: client$i
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=$i
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server
" >> docker-compose.yml
    done
}

add_network() {
    echo "
networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24

" >> docker-compose.yml
}




# =========================================================================

if [ $# -ne 1 ]; then
    echo "Usage: $0 <number_of_clients>"
    exit 1
fi

num_clients=$1


add_compose_header
add_server
add_clients $num_clients
add_network

echo
echo "Successfully created Docker Compose file with: Clients = $num_clients"
