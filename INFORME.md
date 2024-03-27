# Informe TP0: Concurrencia y comunicaciones

### Alumno: Alvarez Windey Juan

### Padrón: 95.242

Para correr el tp

~ make docker-compose-up

Además se deberan descomprimir los CSV dentro de la carpeta .data para que los clientes puedan leerlo

y para bajar los contenedores

~ make docker-compose-down

Detalles y explicaciones a tener en cuenta de cada ejercicio

## Ejercicio 1 y 1.1

Para agregar un nuevo cliente se duplico el cliente preexistente en docker-compose, cambiandole el alias el nombre del container y el ID de variable de entorno.
Por otro lado para la generación de un docker-compose con clientes variables se decidió hacer un script en python que, modificando la variable TOT_CLIENTES, genera un archivo `docker-compose.yaml` con la cantidad de clientes deseados

## Ejercicio 2

Para que al cambiar los archivos de configuración tanto de cliente como servidor y no requiera hacer un nuevo "build", se agregaron ambos archivos de configuración a VOLUMES en cada servicio:

Para el cliente:
`volumes: - ./client/config.yaml:/config/client/config.yaml`

Para el servidor:
`volumes: - ./server/config.ini:/config/server/config.ini`

## Ejercicio 3

Para realizar el script para verificar el servidor con netcat, se opto agregar un servicio nuevo en el docker-compose que usa una imagen de alpine y cuando se levanta (luego del servidor) lanza el comando: 
`sh -c "echo 'Message to verify server with netcat (exercise 3)' | nc -w 3 server 12345" `

Actualmente el servicio se encuentra comentado ya que entorpecia levemente las distintas pruebas de los ejercicios siguientes. Además como el server ya no funciona como un "echo server" no volverá a funcionar al descomentarlo 

## Ejercicio 4

Para manejar la señal `SIGTERM` en el servidor se creo la función `__handle_SIGTERM` que se encarga de cerrar el socket para nuevos clientes y los sockets de los clientes activos. En el cliente simplemente se cierra el socket de conexión con el servidor.

## Ejercicio 5

Para el cambio de lógica en el cliente se comenzó por sacar el timeout, ya que ahora finalizará cuando termine de enviar todas las apuestas. 
El cliente serializará en binario la única apuesta que le llega por variable de entorno, luego la enviará por socket y esperará la confirmación de recepción de la misma por medio de un `ACK` por parte del servidor. 
En el servidor se recibe la apuesta, se guarda en archivo y se envía el `ACK`, luego de esto se procede a un cierre `graceful` teniendo en cuenta los recursos en uso.

Para la parte de serialización, en el cliente, se creo un archivo `protocol.go` que cuenta con la estructura de `Bet` y además con una función de serialización de esta estructura en un array de 70 bytes. La estructura esta definida de la siguiente manera:

```
|- Id -|------ Name ------|------ LastName ------|- Document -|--  Birthdate --|- Number -|
|- 4b -|------  24b ------|------   24b    ------|-    4b    -|--    10b     --|-   4b   -|

Total size = 4 + 24 + 24 + 4 + 10 + 4 = 70b
```

Luego en el servidor también se creó un archivo `protocol.py` que se encarga de recibir una apuesta y parsearla. En el mismo archivo se encuentra también la función que manda `ACK`


## Ejercicio 6

Para este punto en el cliente, todo lo que anteriormente estaba en `protocol.go` se paso a `serialization.go` y en `protocol.go` se dejaron puntualmente las funciones de comunicación con el servidor dado que sino se mezclaba comunicación con serialización de datos.

Cambios en el cliente:

* No recibe más una apuesta por parámetro, ahora las lee de un archivo según corresponde y las va mandando de a una cantidad de `chunks.size`.
* El nuevo flujo es: 
    * Leer `chunks.size` de apuestas por archivos
    * Se serializan todas las apuestas juntas de manera que el array de bytes a enviar queda como: `chunk.size | tot_apuestas`. El primer número se envía para que el servidor sepa de manera dinámica cuantas apuestas va a leer.
    * Una vez enviadas las apuestas se espera recibir el `ACK` que corresponderá a todas las apuestas enviadas
    * El cliente finalizará cuando llegue a EOF o luego de leer menos apuestas que `chunks.size`, ya que indica que se terminó el archivo. A su vez cuando finaliza el cliente mandará otro mensaje al servidor simplemente con un 0, indicando explicitamente que no hay más apuestas que enviar y se debe finalizar.

Cambios en el servidor:

* Ahora el servidor espera recibir más de un mensaje por cliente y para finalizar se fija si la cantidad de apuestas llegadas es 0, que es lo que se usa para indicar que hay que finalizar.
 

## Ejercicio 7

Por una cuestión de simplicidad y tiempos se cambio el Scanner que se usaba en el cliente por un reader, debido a esto el "ACK" paso simplemente a ser el número entero 1.
El cliente luego de conectarse con el servidor le debe enviar el id de su agencia. Esto se hace debido a una cuestión práctica para enviarr/recibir luego los resultados.
También después de enviar todas las apuestas se quedará esperando a que el servidor termine para recibir a los que resultaron ganadores en su agencia, imprimiendo solo la cantidad total de ganadores cuando llegan los datos (llegan tanto ganadores como los documentos de los ganadores).
Esto se recibe como un binario que contiene `| tot_ganadores, gan1, gan2, ... |`. De esta manera la cantidad total de ganadores se usa también como referencia para saber cuantos datos vienen a continuación.
En el servidor, al comienzo de una conexión, se recibe el id del cliente que se guardará junto a su socket. Luego una vez procesadas todas las apuestas, se cargan y se pasan a un record con la siguiente estructura `{ id, {tot_ganadores, [ ganadores ]} }`. Una vez hecho esto se notifica a todos los clientes la cantidad de ganadores de sus respectivas agencias o la ausencia de los mismos.

## Ejercicio 8

Para la parte de concurrencia, del lado del cliente no se cambió nada, dado que esto se implemente de manera opaca hacía los clientes. 
Del lado del servidor, por cada conexión nueva y usando la biblioteca threding, se fue lanzando un nuevo thread con la función `__handle_client_connection` para que fuese atendiendo a el cliente. Ahora se espera a que todos los clientes hayan mandado sus apuestas para luego cada thread pueda procesar el sorteo y enviarle a cada uno de sus clientes la cantidad de ganadores que tuvo. Una vez se envía ese resultado se espera por la finalización de todos los threads para la pronta liberación de recursos.
Una cosa que hubo que tener en cuenta en esta implementación fue el hecho de que tanto para la carga de datos como para la lectura se usaron locks, dado que `store_bets` y `load_bets` no eran *thread safe*. Entonces en el momento que un thread quiere usar el recurso, en este caso abrir un archivo para lectura/escritura, este bloqueará la función que accede a él, haciendo que los demás threads tengan que esperar a que el recurso sea liberado.