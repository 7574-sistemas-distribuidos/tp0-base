if [ "$1" ] 
then  
  clientes=$1
else    
  clientes=2
fi

echo "Se levantaran $clientes clientes"

server_text="version: '3.9'
name: tp0
services:
  server:
    container_name: server
    image: server:latest
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net"

echo "$server_text" > docker-compose-dev.yaml

for ((i = 1; i <= $clientes; i++)); do
  client_text="
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
      - server"
  echo "$client_text" >> docker-compose-dev.yaml
done

network_text="
networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24"

echo "$network_text" >> docker-compose-dev.yaml