# TP0: Docker + Comunicación + Sincronización

En el presente repositorio se provee un ejemplo de cliente-servidor el cual corre en containers con la ayuda de [docker-compose](https://docs.docker.com/compose/). El mismo es un ejemplo práctico brindado por la cátedra para que los alumnos tengan un esqueleto básico de cómo armar un proyecto de cero en donde todas las dependencias del mismo se encuentren encapsuladas en containers. El cliente (Golang) y el servidor (Python) fueron desarrollados en diferentes lenguajes simplemente para mostrar cómo dos lenguajes de programación pueden convivir en el mismo proyecto con la ayuda de containers.

Por otro lado, se presenta una guía de ejercicios que los alumnos deberán resolver teniendo en cuenta las consideraciones generales descriptas al pie de este archivo.

## Instrucciones de uso
El repositorio cuenta con un **Makefile** que posee encapsulado diferentes comandos utilizados recurrentemente en el proyecto en forma de targets. Los targets se ejecutan mediante la invocación de:

* **make \<target\>**:
Los target imprescindibles para iniciar y detener el sistema son **docker-compose-up** y **docker-compose-down**, siendo los restantes targets de utilidad para el proceso de _debugging_ y _troubleshooting_.

Los targets disponibles son:
* **docker-compose-up**: Inicializa el ambiente de desarrollo (buildear docker images del servidor y cliente, inicializar la red a utilizar por docker, etc.) y arranca los containers de las aplicaciones que componen el proyecto.
* **docker-compose-down**: Realiza un `docker-compose stop` para detener los containers asociados al compose y luego realiza un `docker-compose down` para destruir todos los recursos asociados al proyecto que fueron inicializados. Se recomienda ejecutar este comando al finalizar cada ejecución para evitar que el disco de la máquina host se llene.
* **docker-compose-logs**: Permite ver los logs actuales del proyecto. Acompañar con `grep` para lograr ver mensajes de una aplicación específica dentro del compose.
* **docker-image**: Buildea las imágenes a ser utilizadas tanto en el servidor como en el cliente. Este target es utilizado por **docker-compose-up**, por lo cual se lo puede utilizar para testear nuevos cambios en las imágenes antes de arrancar el proyecto.
* **build**: Compila la aplicación cliente para ejecución en el _host_ en lugar de en docker. La compilación de esta forma es mucho más rápida pero requiere tener el entorno de Golang instalado en la máquina _host_.

### Servidor
El servidor del presente ejemplo es un EchoServer: los mensajes recibidos por el cliente son devueltos inmediatamente. El servidor actual funciona de la siguiente forma:
1. Servidor acepta una nueva conexión.
2. Servidor recibe mensaje del cliente y procede a responder el mismo.
3. Servidor desconecta al cliente.
4. Servidor procede a recibir una conexión nuevamente.

### Cliente
El cliente del presente ejemplo se conecta reiteradas veces al servidor y envía mensajes de la siguiente forma.
1. Cliente se conecta al servidor.
2. Cliente genera mensaje incremental.
recibe mensaje del cliente y procede a responder el mismo.
3. Cliente envía mensaje al servidor y espera mensaje de respuesta.
Servidor desconecta al cliente.
4. Cliente vuelve al paso 2.

Al ejecutar el comando `make docker-compose-up` para comenzar la ejecución del ejemplo y luego el comando `make docker-compose-logs`, se observan los siguientes logs:

```
$ make docker-compose-logs 
docker compose -f docker-compose-dev.yaml logs -f
server   | 2023-03-13 03:07:24 DEBUG    Server configuration: {'port': 12345, 'listen_backlog': 5, 'logging_level': 'DEBUG'}
server   | 2023-03-13 03:07:24 INFO     Proceed to accept new connections
server   | 2023-03-13 03:07:24 INFO     Got connection from ('172.25.125.3', 59318)
server   | 2023-03-13 03:07:24 INFO     Message received from connection ('172.25.125.3', 59318). Msg: [CLIENT 1] Message N°1
client1  | time="2023-03-13T03:07:24Z" level=info msg="Client configuration"
server   | 2023-03-13 03:07:24 INFO     Proceed to accept new connections
client1  | time="2023-03-13T03:07:24Z" level=info msg="Client ID: 1"
client1  | time="2023-03-13T03:07:24Z" level=info msg="Server Address: server:12345"
client1  | time="2023-03-13T03:07:24Z" level=info msg="Loop Lapse: 20s"
client1  | time="2023-03-13T03:07:24Z" level=info msg="Loop Period: 5s"
client1  | time="2023-03-13T03:07:24Z" level=info msg="Log Level: DEBUG"
client1  | time="2023-03-13T03:07:24Z" level=info msg="[CLIENT 1] Response from server: Your Message has been received: [CLIENT 1] Message N°1\n"
server   | 2023-03-13 03:07:29 INFO     Got connection from ('172.25.125.3', 59324)
server   | 2023-03-13 03:07:29 INFO     Message received from connection ('172.25.125.3', 59324). Msg: [CLIENT 1] Message N°2
server   | 2023-03-13 03:07:29 INFO     Proceed to accept new connections
client1  | time="2023-03-13T03:07:29Z" level=info msg="[CLIENT 1] Response from server: Your Message has been received: [CLIENT 1] Message N°2\n"
server   | 2023-03-13 03:07:34 INFO     Got connection from ('172.25.125.3', 56502)
server   | 2023-03-13 03:07:34 INFO     Message received from connection ('172.25.125.3', 56502). Msg: [CLIENT 1] Message N°3
server   | 2023-03-13 03:07:34 INFO     Proceed to accept new connections
client1  | time="2023-03-13T03:07:34Z" level=info msg="[CLIENT 1] Response from server: Your Message has been received: [CLIENT 1] Message N°3\n"
server   | 2023-03-13 03:07:39 INFO     Got connection from ('172.25.125.3', 56512)
server   | 2023-03-13 03:07:39 INFO     Message received from connection ('172.25.125.3', 56512). Msg: [CLIENT 1] Message N°4
client1  | time="2023-03-13T03:07:39Z" level=info msg="[CLIENT 1] Response from server: Your Message has been received: [CLIENT 1] Message N°4\n"
server   | 2023-03-13 03:07:39 INFO     Proceed to accept new connections
client1  | time="2023-03-13T03:07:44Z" level=info msg="[CLIENT 1] Loop timeout detected"
client1  | time="2023-03-13T03:07:44Z" level=info msg="[CLIENT 1] Client loop finished"
client1 exited with code 0
```

## Parte 1: Introducción a Docker
En esta primera parte del trabajo práctico se plantean una serie de ejercicios que sirven para introducir las herramientas básicas de Docker que se utilizarán a lo largo de la materia. El entendimiento de las mismas será crucial para el desarrollo de los próximos TPs.

### Ejercicio N°1:
Modificar la definición del DockerCompose para agregar un nuevo cliente al proyecto.

### Ejercicio N°1.1:
Definir un script (en el lenguaje deseado) que permita crear una definición de DockerCompose con una cantidad configurable de clientes.

### Ejercicio N°2:
Modificar el cliente y el servidor para lograr que realizar cambios en el archivo de configuración no requiera un nuevo build de las imágenes de Docker para que los mismos sean efectivos. La configuración a través del archivo correspondiente (`config.ini` y `config.yaml`, dependiendo de la aplicación) debe ser inyectada en el container y persistida afuera de la imagen (hint: `docker volumes`).

### Ejercicio N°3:
Crear un script que permita testear el correcto funcionamiento del servidor utilizando el comando `netcat`. Dado que el servidor es un EchoServer, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado. Netcat no debe ser instalado en la máquina _host_ y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`).

### Ejercicio N°4:
Modificar servidor y cliente para que ambos sistemas terminen de forma _graceful_ al recibir la signal SIGTERM. Terminar la aplicación de forma _graceful_ implica que todos los _file descriptors_ (entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag `-t` utilizado en el comando `docker compose down`).

## Parte 2: Repaso de Comunicación y Sincronización

En esta segunda parte del trabajo práctico se plantea un caso de uso denominado **Lotería Nacional** descompuesto en tres ejercicios. Para la resolución de los mismos deberán utilizarse como base tanto los clientes como el servidor introducidos en la primera parte, con las modificaciones agregadas en el quinto ejercicio.

### Ejercicio N°5:
Modificar la lógica de negocio tanto de los clientes como del servidor para nuestro nuevo caso de uso. 

#### Clientes
Emularán a las 5 _agencias de quiniela_ que participan del proyecto. Deberán recibir como variables de entorno los campos que representan el registro de una persona: nombre, apellido, documento y fecha de nacimiento. Ej.: `NOMBRE=Santiago Lionel`, `APELLIDO=Lorca`, `DOCUMENTO=30904465` y `NACIMIENTO=1999-03-17` respectivamente.

Los campos deben enviarse al servidor para determinar si corresponden a un ganador. Al recibir la respuesta se debe imprimir por log el documento y el resultado obtenido.

#### Servidor
Emulará a la _central de Lotería Nacional_. Deberán recibirse los campos enviados desde los clientes para analizar si corresponden a los de un ganador utilizando la función `is_winner(...)`, para luego responderles. La función `is_winner(...)` es provista por la cátedra y no podrá ser modificada por el alumno.

#### Comunicación:
Se deberá implementar un módulo de comunicación entre el cliente y el servidor donde se maneje el envío y la recepción de los paquetes, el cual se espera que contemple:
* Serialización de los datos.
* Definición de un protocolo para el envío de los mensajes.
* Correcto encapsulamiento entre el modelo de dominio y la capa de transmisión.
* Empleo correcto de sockets, incluyendo manejo de errores y evitando los fenómenos conocidos como [_short read y short write_](https://cs61.seas.harvard.edu/site/2018/FileDescriptors/).
* Garantizar un límite máximo de paquete de 8kB.

### Ejercicio N°6:
Modificar los clientes para que envíen varios registros de personas a la vez (modalidad conocida como procesamiento por _chunks_ o _batchs_). La información de cada de las 5 agencias será simulada por la ingesta de su archivo numerado correspondiente, provisto por la cátedra dentro de `.data/datasets.zip`.
Los _batchs_ de personas deben permitir que el cliente resuelva el estado de varias personas en una misma consulta, acortando tiempos de transmisión y procesamiento.
El servidor, por otro lado, deberá responder con una lista que indique el estado de todas las personas incluidas en la consulta.
Al finalizar, el cliente deberá imprimir por log el porcentaje total de jugadores que hayan ganado en su agencia.

### Ejercicio N°7:
Modificar el servidor actual para que el mismo permita aceptar nuevas conexiones y procesar mensajes en paralelo.
Además, deberá persistir la información de los ganadores utilizando la función `persist_winners(...)`. La función `persist_winners` es provista por la cátedra y no podrá ser modificada por el alumno.
En este ejercicio es importante considerar los mecanismos de sincronización a utilizar para el correcto funcionamiento de la persistencia.

En caso de que el alumno implemente el servidor Python,  deberán tenerse en cuenta las [limitaciones propias del lenguaje](https://wiki.python.org/moin/GlobalInterpreterLock).

### Ejercicio N°8:
Modificar los clientes agregando al final una nueva consulta por el número total de ganadores de todas las agencias.
El servidor deberá ser modificado para contabilizar la cantidad total de ganadores efectivamente almacenados mediante `persist_winners(...)` al momento de recibir la consulta.

En caso de que alguna agencia consulte a la central antes de que esta haya completado el procesamiento de las demás, recibirá la cantidad parcial conocida por el servidor en dicho momento.

## Consideraciones Generales
Se espera que los alumnos realicen un fork del presente repositorio para el desarrollo de los ejercicios, el cual deberá contar con un README que explique cómo correr cada uno de estos. Para la segunda parte del TP también será necesaria una sección donde se explique el protocolo de comunicación implementado y los mecanismos de sincronización utilizado en el último ejercicio. Finalmente, se pide a los alumnos leer atentamente y **tener en cuenta** los criterios de corrección provistos [en el campus](https://campus.fi.uba.ar/course/view.php?id=761).
