# USAGE:
#   ruby build_docker_compose.rb <client-count>
# 
# For example, for 3 clients:
#   ruby build_docker_compose.rb 3

File.open('docker-compose-dev.yaml', 'w') do |file|
    file.write(
        <<-YAML
version: '3'
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
      - testing_net

        YAML
    )

    (1..ARGV.first.to_i).map do |client_id|
        file.write(
            <<-YAML
  client#{client_id}:
    container_name: client#{client_id}
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=#{client_id}
      - CLI_SERVER_ADDRESS=server:12345
      - CLI_LOOP_LAPSE=1m2s
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

            YAML
        )
    end

    file.write(
        <<-YAML
networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24

        YAML
    )
end

