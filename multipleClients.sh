#!/bin/bash

RED='\e[1;31m'
BLUE='\e[1;34m'
GREEN='\e[1;32m'
NC='\033[0m'

environment=${environment:-production}
school=${school:-is out}

while [ $# -gt 0 ]; do

   if [[ $1 == *"-"* ]]; then
        param="${1/-/}"
        declare $param="$2"
   fi

  shift
done


add_client () {
	printf 'client'${1}':
  container_name: client'${1}'
  image: client:latest
  entrypoint: /client
  environment:
    - CLI_ID='${1}'
    - CLI_SERVER_ADDRESS=server:12345
    - CLI_LOOP_LAPSE=1m2s
    - CLI_LOG_LEVEL='${2}'
  networks:
    - testing_net
  depends_on:
    - server\n\n'
}

{
  printf 'version: "3"
services:
  server:
    container_name: server
    image: server:latest
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - SERVER_PORT=12345
      - SERVER_LISTEN_BACKLOG=7
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net\n\n'

  for i in $(seq 1 $clients);
    do 
      add_client $i $log
    done

	printf 'networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24'
} > docker-compose-multipleClients.yaml

echo -e "${GREEN}[SUCCESS]${NC} Docker compose creation successful"
