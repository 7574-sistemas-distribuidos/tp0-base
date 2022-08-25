# TP0: Docker + Comunicación + Sincronización

En el presente repositorio se provee un ejemplo de cliente-servidor el cual corre en containers con la ayuda de [docker-compose](https://docs.docker.com/compose/). El mismo es un ejemplo práctico brindado por la cátedra para que los alumnos tengan un esqueleto básico de cómo armar un proyecto de cero en donde todas las dependencias del mismo se encuentren encapsuladas en containers. El cliente (Golang) y el servidor (Python) fueron desarrollados en diferentes lenguajes simplemente para mostrar cómo dos lenguajes de programación pueden convivir en el mismo proyecto con la ayuda de containers.

Por otro lado, se presenta una guía de ejercicios que los alumnos deberán resolver teniendo en cuenta las consideraciones generales descriptas al pie de este archivo.

## Instrucciones de uso
El repositorio cuenta con un **Makefile** que posee encapsulado diferentes comandos utilizados recurrentemente en el proyecto en forma de targets. Los targets se ejecutan mediante la invocación de:

* **make \<target\>**
El target principal a utilizar es **docker-compose-up** el cual permite inicializar el ambiente de desarrollo (buildear docker images del servidor y client, inicializar la red a utilizar por docker, etc.) y arrancar los containers de las aplicaciones que componen el proyecto.

Los targets disponibles son:
* **docker-compose-up**: Inicializa el ambiente de desarrollo (buildear docker images del servidor y client, inicializar la red a utilizar por docker, etc.) y arranca los containers de las aplicaciones que componen el proyecto.
* **docker-compose-down**: Realiza un `docker-compose stop` para detener los containers asociados al compose y luego realiza un `docker-compose down` para destruir todos los recursos asociados al proyecto que fueron inicializados. Se recomienda ejecutar este comando al finalizar cada ejecución para evitar que el disco de la máquina host se llene.
* **docker-compose-logs**: Permite ver los logs actuales del proyecto. Acompañar con grep para lograr ver mensajes de una aplicación específica dentro del compose.
* **docker-image**: Buildea las imágenes a ser utilizadas tanto en el client como el server. Este target es utilizado por **docker-compose-up**, por lo cual se lo puede utilizar para testear nuevos cambios en las imágenes antes de arrancar el proyecto.
* **build**: Compila la aplicación cliente en el host en lugar de Docker. La compilación de esta forma es mucho más rápida pero requiere tener el entorno de Golang instalado en la máquina.

### Servidor
El servidor del presente ejemplo es un EchoServer: los mensajes recibidos por el cliente son devueltos inmediatamente. El servidor actual funciona de la siguiente forma:
1. Servidor acepta una nueva conexión.
2. Servidor recibe mensaje del cliente y procede a responder el mismo.
3. Servidor desconecta al cliente.
4. Servidor procede a recibir una conexión nuevamente.

Al ejecutar el comando `make docker-compose-up` para comenzar la ejecución del ejemplo y luego el comando `make docker-compose-logs`, se observan los siguientes logs:

```
efeyuk@Helena:~/Development/tp0-base$ make docker-compose-logs
docker-compose -f docker-compose-dev.yaml logs -f
Attaching to client1, server
server     | 2020-04-10 23:10:54 INFO     Proceed to accept new connections.
server     | 2020-04-10 23:10:55 INFO     Got connection from ('172.24.125.3', 60392).
server     | 2020-04-10 23:10:55 INFO     Message received from connection. ('172.24.125.3', 60392). Msg: b'[CLIENT 1] Message number 1 sent.'
server     | 2020-04-10 23:10:55 INFO     Proceed to accept new connections.
server     | 2020-04-10 23:11:05 INFO     Got connection from ('172.24.125.3', 60400).
server     | 2020-04-10 23:11:05 INFO     Message received from connection. ('172.24.125.3', 60400). Msg: b'[CLIENT 1] Message number 2 sent.'
client1    | time="2020-04-10T23:10:55Z" level=info msg="[CLIENT 1] Message from server: Your Message has been received: b'[CLIENT 1] Message number 1 sent.'"
client1    | time="2020-04-10T23:11:05Z" level=info msg="[CLIENT 1] Message from server: Your Message has been received: b'[CLIENT 1] Message number 2 sent.'"
server     | 2020-04-10 23:11:05 INFO     Proceed to accept new connections.
server     | 2020-04-10 23:11:15 INFO     Got connection from ('172.24.125.3', 60406).
server     | 2020-04-10 23:11:15 INFO     Message received from connection. ('172.24.125.3', 60406). Msg: b'[CLIENT 1] Message number 3 sent'
client1    | time="2020-04-10T23:11:15Z" level=info msg="[CLIENT 1] Message from server: Your Message has been received: b'[CLIENT 1] Message number 3 sent.'"
server     | 2020-04-10 23:11:35 INFO     Message received from connection.
client1    | time="2020-04-10T23:12:05Z" level=info msg="[CLIENT 1] Main loop finished."
client1 exited with code 0
```

## Parte 1: Introducción a Docker
En esta primera parte del trabajo práctico se plantean una serie de ejercicios que sirven para introducir las herramientas básicas de Docker que se utilizarán a lo largo de la materia. El entendimiento de las mismas será crucial para el desarrollo de los próximos TPs.

### Ejercicio N°1:
Modificar la definición del DockerCompose para agregar un nuevo cliente al proyecto.

### Ejercicio N°1.1:
Definir un script (en el lenguaje deseado) que permita crear una definición de DockerCompose con una cantidad configurable de clientes.

### Ejercicio N°2:
Modificar el cliente y el servidor para lograr que realizar cambios en el archivo de configuración no requiera un nuevo build de las imágenes de Docker para que los mismos sean efectivos. La configuración a través del archivo debe ser inyectada al ejemplo y persistida afuera del mismo (hint: `docker volumes`).

### Ejercicio N°3:
Crear un script que permita testear el correcto funcionamiento del servidor utilizando el comando `netcat`. Dado que el servidor es un EchoServer, se debe enviar un mensaje el servidor y esperar recibir el mismo mensaje enviado. Netcat no debe ser instalado en la máquina host y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`).

### Ejercicio N°4:
Modificar el cliente y el servidor para que el programa termine de forma gracefully al recibir la signal SIGTERM. Terminar la aplicación de forma gracefully implica que todos los sockets y threads/procesos de la aplicación deben cerrarse/joinearse antes que el thread de la aplicación principal muera. Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag `-t` utilizado en el comando `docker-compose down`).

## Parte 2: Repaso de Comunicación y Sincronización

En esta segunda parte del trabajo práctico se plantea un caso de uso denominado **Lotería Nacional** descompuesto en tres ejercicios. Para la resolución de los mismos deberán utilizarse como base tanto los clientes como el servidor introducidos en la primera parte, con las modificaciones agregadas en el quinto ejercicio.

### Ejercicio N°5:
Modificar la lógica de negocio tanto de los clientes como del servidor para nuestro nuevo caso de uso. 

Por el lado de los clientes (quienes emularán _agencias de quiniela_) deberán recibir como variables de entorno los siguientes datos de una persona: nombre, apellido, documento y fecha de nacimiento. Dichos datos deberán ser enviados al servidor para saber si corresponden a los de un ganador, información que deberá loguearse. Por el lado del servidor (que emulará la _central de Lotería Nacional_), deberán recibirse los datos enviados desde los clientes y analizar si corresponden a los de un ganador utilizando la función provista `is_winner(...)`, para luego responderles.

Deberá implementarse un módulo de comunicación entre el cliente y el servidor donde se maneje el envío y la recepción de los paquetes, el cual se espera que contemple:
* Serialización de los datos.
* Definición de un protocolo para el envío de los mensajes.
* Correcto encapsulamiento entre el modelo de dominio y la capa de transmisión.
* Empleo correcto de sockets, incluyendo manejo de errores y evitando el fenómeno conocido como _short-read_.

### Ejercicio N°6:
Modificar los clientes para que levanten los datos de los participantes desde los datasets provistos en los archivos de prueba en lugar de las variables de entorno. Cada cliente deberá consultar por todas las personas de un mismo set (los cuales representan a los jugadores de cada agencia) en forma de batch, de manera de poder hacer varias consultas en un solo request. El servidor por otro lado deberá responder con los datos de todos los ganadores del batch, y cada cliente al finalizar las consultas deberá loguear el porcentaje final de jugadores que hayan ganado en su agencia.

### Ejercicio N°7:
Modificar el servidor actual para que el mismo permita procesar mensajes y aceptar nuevas conexiones en paralelo. Además, deberá comenzar a persistir la información de los ganadores utilizando la función provista `persist_winners(...)`. Considerar los mecanismos de sincronización a utilizar para el correcto funcionamiento de dicha persistencia.

En caso de que el alumno desee implementar un nuevo servidor en Python,  deberán tenerse en cuenta las [limitaciones propias del lenguaje](https://wiki.python.org/moin/GlobalInterpreterLock).

### Ejercicio N°8:
Agregar en los clientes una consulta por el número total de ganadores de todas las agencias, por lo cual se deberá modificar el servidor para poder llevar el trackeo de dicha información.

En caso de que alguna agencia consulte a la central antes de que esta haya completado el procesamiento de las demás, deberá recibir una respuesta parcial con el número de agencias que aún no hayan finalizado su carga de datos y volver a consultar tras N segundos.

## Consideraciones Generales
Se espera que los alumnos realicen un fork del presente repositorio para el desarrollo de los ejercicios, el cual deberá contar con un README que explique cómo correr cada uno de estos. Para la segunda parte del TP también será necesaria una sección donde se explique el protocolo de comunicación implementado y los mecanismos de sincronización utilizado en el último ejercicio. Finalmente, se pide a los alumnos leer atentamente y **tener en cuenta** los criterios de corrección provistos [en el campus](https://campus.fi.uba.ar/course/view.php?id=761).
