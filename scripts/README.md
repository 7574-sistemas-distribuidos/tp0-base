Todos los scripts se deben correr parados desde el root del projecto.

- docker-compose-client-generator se encarga de generar el docker compose con la cantidad correcta de clientes y corresponde al punto 2.

- test-EchoServer hace un make docker-compose-up con 1 solo cliente, y luego verifica mandando desde este cliente un mensaje que el servidor responda correctamente. Antes de terminar se hace un docker-compose-down. Este script corresponde al punto 3.