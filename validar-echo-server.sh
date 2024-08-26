#!/bin/bash

signal="healthcheck"
image_name="alpine:edge"
container_name="server"
container_network="tp0_testing_net"
server_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' --type=container $container_name)
server_port=12345

container_response=$(docker run -q --network=$container_network $image_name sh -c "echo -n $signal | nc $server_ip $server_port 2>/dev/null")
if [[ "$container_response" == "$signal" ]]; then
    echo "action: test_echo_server | result: success"
else
    echo "action: test_echo_server | result: fail"
fi
