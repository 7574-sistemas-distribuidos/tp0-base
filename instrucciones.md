El programa ```create_docker_compose.py``` crea un archivo copiando ```docker-compose-dev.yaml```, y segun el numero recibido por parametro, escribe en el archivo la cantidad de clientes deseada, y finalmente, reemplaza el archivo.

Para ejecutar, correr la siguiente instruccion por linea de comandos:  
``` python3 create-docker-compose.py X ```  
Siendo X el numero de clientes a declarar

## Ejercicio 2
Para comprobar el funcionamiento del volumen, una vez que corro `make docker-compose-up`, modifico los valores de puerto de los archivos `config.ini` para el server, y `config.yaml` para los clientes, luego, cuando vuelvo a ver los logs con `make docker-compose-logs`, veo que los clientes pudieron comunicarse con el server ambos utilizando el nuevo puerto.

