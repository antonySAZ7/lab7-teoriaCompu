antony saz 24710
Problema 1: Simplificacion de gramaticas
Se desarrollo un programa en Python que carga archivos de texto con producciones de una gramatica,
valida cada linea con una expresion regular y elimina producciones epsilon.
Validacion de producciones
El programa acepta producciones con un no terminal en el lado izquierdo, una flecha -> o una flecha
unicode, y una o mas alternativas separadas por el operador OR |. Si una linea no cumple el formato,
la ejecucion se detiene e indica el numero de linea donde se encontro el error.
Eliminacion de epsilon
Primero se encuentran los simbolos anulables. Un simbolo es anulable si produce epsilon
directamente o si todos los simbolos de alguno de sus cuerpos tambien son anulables. Despues, para
cada produccion con m simbolos anulables, se generan los 2^m casos posibles conservando o
eliminando dichos simbolos. Las producciones epsilon originales se remueven. Si el simbolo inicial es
anulable, se agrega un nuevo simbolo inicial para conservar la capacidad de generar epsilon.



