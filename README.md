# Docker Compose Init
El siguiente ejemplo es un cliente-servidor el cual corre en containers 
con la ayuda de [docker-compose](https://docs.docker.com/compose/). El presente
repositorio es un ejemplo práctico brindado por la cátedra para que los alumnos
tengan un esqueleto básico de cómo armar en donde todas las dependencias del 
mismo se encuentren encapsuladas en containers.

El cliente (golang) y el servidor (python) fueron desarrollados en diferentes 
lenguajes simplemente para mostrar cómo dos lenguajes de programación pueden 
convivir en el mismo proyecto con la ayuda de containers.

## Instrucciones de uso
El repositorio cuenta con un Makefile que posee encapsulado diferentes comandos
utilizados recurrentemente en el proyecto en Makefile targets. 

El comando principal a utilizar el **docker-compose-up** el cual permiten inicializar
el ambiente de desarrollo (buildear docker images del servidor y client, inicializar
la red a utilizar por docker, etc.) y arrancar los containers de las aplicaciones 
que componen el proyecto. 

Otros targets de utilizar son:
* **make docker-compose-down**: Realiza un docker compose stop para detener los containers
asociados al compose y luego realiza un docker compose down para destruir todos los 
recursos asociados al proyecto que fueron inicializados durante el **docker-compose-up**
target.
* **make docker-compose-logs**: Permite ver los logs actuales del proyecto. Acompañar con grep
para lograr ver mensajes de una aplicación específica dentro del compose
* **make docker-image**: Buildea las imágenes a ser utilizadas tanto en el client como el server.
Este target es utilizado por **docker-compose-up**, por lo cual se lo puede utilizar para 
testear nuevos cambios en las imágenes antes de arrancar el proyecto.
* **make build**: Compila la aplicación cliente en la máquina en vez de docker. La compilación
de esta forma es mucho más rápida pero requiere tener el entorno de golang instalado en la 
máquina.

# Ejercicios Prácticos
La idea de los siguientes ejercicios prácticos consisten en que los alumnos 
se familiaricen con ambientes de desarrollo desarrollados en docker/docker-compose,
poniéndo énfasis en la automatización de cualquier parte del proyecto y la portabilidad
del mismo (evitar que el usuario que usa el proyecto tenga que instalar otra dependencia
más que docker/docker-compose para correr el proyecto) 

## Ejercicio N°1:
Modificar la definición del docker-compose para agregar un nuevo cliente al proyecto.

## Ejercicio N°1.1 (Opcional):
Definir un script (en el lenguaje deseado) que permita crear una definición de 
docker-compose con N cantidad de clientes.

## Ejercicio N°2:
Modificar el cliente y el servidor para lograr que la configuración de ambas
aplicaciones sea leída por tanto por variables de ambiente como 
por archivo de configuración. Configuración por archivo de configuración
debe ser _injectada_ al ejemplo y persistida afuera del mismo. (Hint: docker volumes)

## Ejercicio N°3:
Crear un script que permita conectarse con el servidor utilizando el comando netcat.
Netcat no debe ser instalado en la maquina y no se puede exponer puertos del 
servidor para realizar la comunicación. (Hint: docker network)



