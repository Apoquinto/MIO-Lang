<div align="center">

![logoPlaceholder](/Imagenes/logo.png)

</div>

## ¿Mio?

Mio es un lenguaje de programación diseñado como práctica complementaria para las actividades de la asignatura de teoria de la computación, este lenguaje solo llega a abarcar las partes de un compilador que corresponden a el analizador léxico y el analizador sintactico.
Como tal todo esta construido con python sin uso de ninguna libreria externa.

## Objetivos
- __pseudoCLI.__ Se busca crear una pequeña interfaz de linea comandos para darle más dinamismo a la ejecucion de MIO.

- __Analizador Léxico.__ Se busca crear un analizador léxico que permita la identificación de tokens de distinto tipo de un arhivo fuente .mio, como tal se solicita que recopile dicha información en dos archivos, un .lex que contendra como tal un stack para el analizador sintáctico y un .sim que contrendra la tabla de identificadores de los distintos tipos de datos de MIO.

- __Analizador Sintáctico.__ Por último, se debe de tener en cuenta que el programa pueda identificar errores al momento de compilar.

## Requerimientos
Como se mencionó anteriormente, Mio esta construido con python, asi que se necesita tener en la computadora python 3, no se requiere que se utilice un sistema operativo en particular.

## Quick start
Para probar el proyecto actual de MIO, basta con que tengas la carpeta principal del proyecto, ya sea descargandola desde el repositorio del proyecto o mediante la carpeta misma.

Lo primero que tenemos que hacer es ejecutar la pseudoCLI de MIO: __MiCLI__, para ello ejecutamos el comando `python runMIO,py`.

Una vez ejecutado el comando, ya estaras en la pseudoCLI del proyecto, como tal el CLI se configura para agarrar el directorio donde se ejecuta, por lo que puedes compilar los archivos de MIO utilizando el comando `analex (nombre del archivo)` aunque recuerda que debe de tener la terminación `.mio`, si no el CLI lo rechazará.

Cuando se compile un archivo, se generarán dos los dos archivos que se mencionaron antes.

Ahora mismo el Analizador sintactico no funciona, por lo que no es posible la evaluación de si el código funciona o no, pero muy pronto estará disponible :D

Si quieres dejar de usar MIiCLI, solo tienes que usar el comando `\q` y con ello volverás a tu shell normal.

También puedes usar el comando `\h` para recibir más información sobre lo que se puede hacer con MiCLI (actualmente no mucho :c).

## Documentación.
En caso de que quieras comprobar las pruebas que se han hecho, en la carpeta docs del proyecto hay Jupyter Nootebooks con pruebas individuales para cada una de las partes del proyecto, aunque si quieres ver el código en su máximo esplendor siempre puedes ir a la carpeta src, que es donde esta el código principal hecho en python y comentado.