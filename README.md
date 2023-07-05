# EvAM-Tools-Web-Tester

Esta herramienta ha sido desarrollada para la prueba y validación de los casos de uso presentes en la aplicación de  [EvAM-Tools](https://www.iib.uam.es/evamtools/) por Laurentiu Mihai Adetu.


# Configuración del entorno e instalación

Para empezar es necesario configurar un fichero **.env** en base al fichero **.env.example** donde los campos son:
* BINARY_LOC: localización del ejecutable de firefox en caso de utilizar  una versión ESR.
* URL: dirección sobre la que se ejecutarán las pruebas en caso de realizarlas sobre producción o en local
* DATA_FILES_PATH: dirección de la carpeta con datos adicionales necesarios para las pruebas.
* TESTS_SELECTOR_PATH: dirección del fichero de configuración para las pruebas.

Una vez configurado dicho fichero es necesario instalar los requisitos presentes en el requirements.txt. Se recomienda instalarlos en un entorno virtual para evitar problemas con las versiones.

## Instalación y configuración de Firefox-esr

Para la ejecución de las pruebas haciendo uso de firefox-esr (Recomendado) es necesario descargar la versión que se quiera ejecutar de [Firefox ESR ](https://www.mozilla.org/es-ES/firefox/enterprise/)
Una ves descargada la versión es necesario copiar la dirección del ejecutable firefox a la variable referenciada anteriormente.
En caso de utilizar una versión normal de firefox se puede obviar este paso (No recomendado).

## Instalación y configuración de Chrome

Para la configuración de Chrome basta con instalarlo en linux de manera normal con APT

## Ejecución de la herramienta
### Configuración del fichero .JSON
El primer fichero que se debe modificar para la ejecución el el fichero de configuración basado en el **config.json.example** el cual muestra como construir el fichero para la selección de pruebas a ejecutar.
### Ejecución de la herramienta

python3 ./src/evam-tools-web-tester ---tests_list {group_name} --browser {browser_name}

* group_name: nombre del grupo de pruebas a ejecutar presente en el fichero de configuración **Config.json**
* browser_name: nombre del buscador contra el que se van a ejecutar las pruebas.

## Creación de nuevas pruebas
Para agregar una nueva prueba se debe partir del fichero **./src/tests/test_template.py** y no alterar los nombres de
la clase ni de la función ya que no funcionará la ejecución.
Una vez creada la prueba basta con dejarla en el módulo **tests** e incluirla en el grupo que se va a ejecutar en el 
fichero de configuración.