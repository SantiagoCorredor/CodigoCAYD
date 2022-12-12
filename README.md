# CodigoCAYD
Soporte de códigos realizados para CAYD incluye simulaciones de un codigo de línea, un código de canal, una modulación digital, una simulación de un multiplexado y una simulación del esquema de acceso multiple

El programa consta de una interfaz gráfica que ayuda a mejorar a hacer más sencillo la simulación junto a su entendimiento.

Programa desarrollado en Python junto a sus dependencias y librerías, este programa presenta una interfaz gráfica correspondiente a un menú donde el usuario 
es capaz de seleccionar cual de las funciones desea usar, puede elegirse entre: 1) Simulación de código (Código Manchester) de línea junto a una simulación de 
la conformación de una banda base, 2) Codificador de Canal Hamming (7,11) el cual por medio de la entrega de una serie de bits dados por el usuario (7 bits) a 
la interfaz gráfica el programa encuentra su equivalente codificado, además, este programa es capaz de encontrar si una codificación ya realizada tiene un error 
y también le corrige. 3) Posee un simulador de 16-QAM el cual puede recibir una cadena de datos los cuales modulará y presentará la señal modulada, junto a la de 
entrada y la modulada con ruido, luego, expondrá el diagrama de constelación junto a la llegada de cada punto enviado. 4) Simulación de un esquema de multiplexación 
el cual puede ser de hasta doce señales diferentes, el usuario elige cuantas señales existirán por medio de la interfaz gráfica, esto lo realiza por medio de una 
serie de tonos modulados en AM y presentando sus respectivas gráficas, junto a la señal de salida y su espectro de potencia. 5) Simulación de un esquema de acceso 
múltiple, el cual se presentará por medio de señales moduladas en AM.

El archivo de trabajo principal es : Main.py
Las librerias asociadas se encuentran en : venv
