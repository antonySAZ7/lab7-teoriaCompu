# Laboratorio 7 - Simplificacion de gramaticas

Programa en Python para cargar gramaticas desde archivos de texto, validar sus producciones y eliminar producciones epsilon.

## Ejecucion

```bash
python src/grammar_simplifier.py grammars/gramatica1.txt grammars/gramatica2.txt
```

Tambien puede ejecutarse con un solo archivo:

```bash
python src/grammar_simplifier.py grammars/gramatica1.txt
```

## Formato aceptado

Cada linea debe tener esta forma:

```txt
A -> aB | b | ε
```

Reglas usadas por el programa:

- El lado izquierdo debe ser una sola letra mayuscula.
- Se acepta `->` o `→` como flecha.
- Las alternativas del lado derecho se separan con `|`.
- Los no terminales son letras mayusculas individuales.
- Los terminales son letras minusculas o digitos.
- Epsilon puede escribirse como `ε`, `epsilon` o `eps`.

Si una linea esta mal escrita, el programa se detiene y muestra el numero de linea donde encontro el error.

## Video

Enlace del video no listado de YouTube:

Pendiente: pegar aqui el enlace despues de grabar la demostracion.

## Sugerencia para la demostracion

1. Ejecutar el programa con las dos gramaticas correctas.
2. Modificar temporalmente una produccion, por ejemplo:

```txt
S 0A0 | 1B1
```

3. Ejecutar de nuevo para mostrar que la validacion detecta el error.
4. Corregir la produccion y ejecutar otra vez.

## Archivos

- `src/grammar_simplifier.py`: programa principal.
- `grammars/gramatica1.txt`: primera gramatica de prueba.
- `grammars/gramatica2.txt`: segunda gramatica de prueba.
- `docs/`: carpeta para documentos PDF de respuestas que no involucren codigo.
