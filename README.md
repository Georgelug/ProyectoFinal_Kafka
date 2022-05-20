# **Kafka**
## An implementation _Producer-Consumer_ pattern design of Kafka

## **Introduccion**
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

## **Referencias**
- Kreps, J. K., Narkhede, N. N., & Rao, J. R. (s. f.). Kafka: a Distributed Messaging System for Log Processing. http://notes.stephenholiday.com/. Recuperado 19 de mayo de 2022, de <http://notes.stephenholiday.com/Kafka.pdf>

-  Producer Consumer. (s. f.). Java Design Patterns. Recuperado 19 de mayo de 2022, de <https://java-design-patterns.com/patterns/producer-consumer/>