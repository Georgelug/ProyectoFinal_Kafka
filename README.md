# **Kafka**
## An implementation _Producer-Consumer_ pattern design of Kafka
## Autores
- Esparza Fuentes Jorge Luis
- González Alcalá Octavio
- Sánchez Pérez Omar Alejandro

**Link del trabajo escrito:** <https://docs.google.com/document/d/1yV3hRTTEWkqr1ExIX4gx8akcFsGr-iqZEqPzBlWe-V8/edit?usp=sharing>

## **Introducción**
El proyecto que se pretende realizar, es una simulación del sistema Kafka, enfocado en el patrón de diseño publisher-consumer, el cual consistirá en implementar dos servers los cuales fungirán como brokers y 4 clientes los cuales 2 serán de tipo producer y el resto de tipo consumer. Por lo tanto la dinámica será la siguiente:

![fuente: http://notes.stephenholiday.com/Kafka.pdf](/images/Kafka.png "Diagrama que ilustra el funcionamiento de Kafka")
Fuente: <http://notes.stephenholiday.com/Kafka.pdf>

Por lo tanto, para llevar a cabo el proyecto, se propone que los servers sean pequeñas API’s y cada una tenga su lista donde se puedan guardar temporalmente  los tópicos, por cuestiones de tiempo y porque no es el objetivo del proyecto, no se podrá implementar una base de datos para poder guardar de forma permanente, por lo tanto estos por medio de peticiones los clientes de tipo consumer podrán obtener los tópicos y finalmente los producers de igual forma por medio de peticiones, podrá editar, crear y eliminar tópicos.

Dicho de otra forma, las funcionalidades de los clientes y server son:

### **Descripción de la API (brokers)**
Los brokers serán API los cuales a su vez serán servidores, por lo tanto estos servidores serán simples scripts tipo serverless que se ejecutarán en localhost y darán servicio a los clientes tanto de tipo producer como de tipo consumer. Ahora bien, el server fungirá tanto como API y a su vez como una especie de base de datos el cual consistirá en un objeto literal o diccionario donde se guardará una clave (tópico) y una lista de string (mensaje), por lo tanto si el producer publica un tópico existente, con base en este mismo solo se anexará a la lista de mensajes que tenga ese mismo tópico y en caso contrario si no existe el tópico, este se anexa como clave dentro del diccionario de la API y se crea una nueva lista junto con el mensaje que se desea agregar. Ejemplo:

![ejemplo 1](/images/ej1.png "Ejemplo de diccionario con tópicos")

Como podemos observar en la imagen anterior se tiene un diccionario con algunos tópicos y sus correspondientes listas de mensajes. Por lo tanto si un producer quiere publicar un nuevo tópico con un nuevo mensaje, entonces deberá agregar una nueva clave (por ejemplo cualquier número distinto de los que ya se tienen) y automáticamente se asocia una lista con el mensaje nuevo.

![ejemplo 2](/images/ej2.png "Ejemplo de diccionario con tópicos nuevos")

Ahora bien para la parte de la distribución o balance de carga del consumo de los tópicos, para esto los objetos de tipo brokers tendrán como atributo un identificador numérico y otro el cual indique el estado donde indique si está en uso o está en estado de reposo. Por lo tanto, por ejemplo si un consumidor está en comunicación con uno de los brokers a implementar entonces su estado cambiaria a ocupado y por lo tanto no podrá ser usado por otros consumers, no obstante quedaría libre el otro broker por lo tanto el otro consumer directamente entraría en comunicación con este otro.

![ejemplo 2](/images/claseBroker.png "Clase broker")

### **Descripción de los clientes tipo producer**
Los producers simplemente son clientes que tienen la funcionalidad de publicar en un broker un tópico con una lista de mensajes, por lo tanto, como se mencionó anteriormente, se entabla comunicaciones con los dos brokers a implementar y se publican los tópicos anexandolos a  los correspondientes diccionarios de los brokers, para luego ser consumidos por los clientes de tipo consumer. Estos clientes se ejecutarán de igual forma en el localhost y se utilizará el protocolo http y a su vez los verbos GET, PUT, DELETE y POST.

### **Descripción de los clientes tipo consumer**
Los consumers simplemente son clientes que tienen la funcionalidad de consumir en un broker un mensaje de un tópico determinado, por lo tanto, como se mencionó anteriormente se realizarán los siguientes pasos:
Se entabla comunicaciones con alguno de los dos brokers a implementar con base en su disponibilidad.
Una vez entablada la comunicación, el consumer realiza una petición al broker para obtener todos los tópicos disponibles.
El consumer elige un topic
Se realiza otra petición para obtener todos los mensajes del topic elegido
El consumer elige el mensaje que desea consumir, en caso de que sea solo uno se omite este paso y simplemente se le asigna el que se tiene asignado al topic dentro del broker.
Se le asigna el mensaje elegido para ser consumido, es decir se realiza un set al atributo message para asignar el mensaje elegido.

## **Diagrama de clases**
Con base en el patrón de diseño producer-consumer, se tiene la siguiente propuesta de diseño para la implementación de este sistema.
![Patrón de diseño publisher-consumer](https://java-design-patterns.com/patterns/producer-consumer/etc/producer-consumer.png "Patrón de diseño original, llamado publisher-consumer")

Fuente: <https://java-design-patterns.com/patterns/producer-consumer/>

Ahora bien, el siguiente diagrama determina las clases a implementar en este proyecto y como estas interactuan entre ellas:

![Patrón de diseño publisher-consumer](/images/diagramaClases.png "Patrón de diseño original, llamado publisher-consumer")

## **Pipeline** 
**Consumer**
1. elegir broker 
2. hacer peticion al server 
3. del lado del broker se cambia el estado a True el estado de activo con la funcion setActiveStatus(self, status) 
4. se le muestra al consumer la lista de topicos, usando la funcion getTopics(self) 
5. el usuario elige el topico, ese valor se guarda para utilizarse en el siguiente paso 
6. se muestra los mensajes, con el valor recibido antes, se manda a llamar la funcion getTopic_toClient(self,key) 
7. el usuario ingresa el número del mensaje (índice de la lista) que elige para consumir, y se guarda ese valor para el siguiente paso 
8. se muestra en pantalla el mensaje que el usuario eligió para consumir con base en el valor anterior y el valor del tópico se manda a llamar la funcionalidad getMessage(self,key,indexMessage = 0) 

**Producer** 
1. el usuario ingresa el tópico, ese valor se guarda 
2. el usuario ingresa el mensaje, ese valor se guarda
3. el usuario da click en el submit, hace petición al server y se manda la info [tópico, mensaje] y se manda a llamar la función addNewMessage(self, topic, message)

## **Tecnologías utilizadas** 
- **Flask**: Framework utilizado para crear las aplicaciones web de los clientes que utilizan el broker.(utilizada solo en  los clientes Publisher y Consumer)
- **Bootstrap**: Framework utilizado para el diseño del FrontEnd.
- **JQuery**: Plugin necesario para el correcto funcionamiento de Bootstrap.
- **Popper**: Plugin necesario para el correcto funcionamiento de Bootstrap.
- **ZMQ**: con este módulo, se pudo realizar la parte del backend, para conectar y comunicar los clientes Producer y Consumer con el broker, donde los clientes hacen peticiones y el server con brokers responde esas peticiones.
- **Git y Github**: se manejo git como repositorio local para cada integrante y github como repositorio remoto para el trabajo colaborativo. se tiene la rama main, para la entrega final, develop, sobre la cual se realizarán los merge y ramas función, sobre las cuales se estarán trabajando.

## **Manual de usuario**
### Descargar programa
git clone https://github.com/Georgelug/ProyectoFinal_Kafka.git

cd ProyectoFinal_Kafka

### Consideraciones
Nota 1: antes de ejecutar, por favor de modificar la ruta absoluta con base en la ruta donde se ubique el proyecto clonado o descargado, de esta forma se podrá importar el módulo que contiene las clases que se van a implementar en este proyecto, tanto en el main.py de la carpeta broker, producer como del consumer.

![sys.path.insert(0,<insertar aqui ruta absoluta>)](/images/sysPath.png "Ejemplo de ruta absoluta")

Como se puede ver en la imagen anterior, la función insert lo que hace es agregar en la lista del path que utiliza el intérprete de python para ejecutar el código, por lo que al agregar esta ruta se debe utilizar la función insert pasándole como parámetro la posición (la primera) y la ruta absoluta donde se encuentra la carpeta tools.

Nota 2: existe un bug durante la ejecución del server de brokers por lo que al presionar ctrl+c no se podrá terminar la ejecución por lo que para poder “apagar” el server se tendrá que cerrar o si se está utilizando VS code darle en kill terminal y de esta forma se podrá finalizar la ejecución. Por lo tanto, para volver a “prender” el server se tendrá que volver a iniciar una nueva terminal y realizar los pasos detallados en la siguiente sección (ver Ejecutar los Brokers)

![kill terminal](/images/killTerminal.png "kill terminal")

Nota 3: Antes de realizar la ejecución del programa principal del consumer (main.py), es necesario realizar un cambio en la línea 59.

![ruta absoluta del archivo Buttons.html](/images/errorHTML.png "cambio de ruta absoluta")

Este cambio consiste en colocar la ruta absoluta del archivo Buttons.html, el cual contiene los botones con los que puede interactuar el usuario (Consumer).

### Instalar dependencias
En la carpeta ProyectoFinal_Kafka ejecutar el siguiente comando
pip install -r requirements.txt

### Entrar a la carpeta de trabajo
cd src 
Ejecutar los Brokers
En la carpeta src
cd Broker
python3 main.py
todas las interacciones que sean realizadas por los clientes, serán reflejadas en el broker

Si se desea hacer una carga inicial de mensajes
python3 main.py true

### Ejecutar Producer
En la carpeta src
cd Producer
python3 main.py

ahora deberás acceder a la url que indica la terminal desde tu navegador de confianza, una vez y el broker este activo, podrás estar enviando mensajes al broker

### Ejecutar Consumer
En la carpeta src
cd Consumer
python3 main.py

ahora deberás acceder a la url que indica la terminal desde tu navegador de confianza, una vez y el broker este activo, se podrá recibir los tópicos y mensajes según indique el usuario.


## **Referencias**
- Kreps, J. K., Narkhede, N. N., & Rao, J. R. (s. f.). Kafka: a Distributed Messaging System for Log Processing. http://notes.stephenholiday.com/. Recuperado 19 de mayo de 2022, de http://notes.stephenholiday.com/Kafka.pdf 

- Producer Consumer. (s. f.). Java Design Patterns. Recuperado 19 de mayo de 2022, de https://java-design-patterns.com/patterns/producer-consumer/ 

- Welcome to Flask — Flask Documentation (2.1.x). (s. f.). Flask. Recuperado 2 de junio de 2022, de https://flask.palletsprojects.com/en/2.1.x/ 

- ZeroMQ. (s. f.). ZMQ. Recuperado 2 de junio de 2022, de https://zeromq.org/ 

- Otto, M. J. T. (s. f.). Introduction. Bootsrap. Recuperado 2 de junio de 2022, de https://getbootstrap.com/docs/4.6/getting-started/introduction/ 

- WTForms — WTForms Documentation (3.0.x). (s. f.). WTF. Recuperado 2 de junio de 2022, de https://wtforms.readthedocs.io/en/3.0.x/ 

