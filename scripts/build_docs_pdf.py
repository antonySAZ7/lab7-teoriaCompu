from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "respuestas_laboratorio7.pdf"


def build_pdf():
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Laboratorio 7 - Respuestas", styles["Title"]),
        Spacer(1, 12),
        Paragraph("Problema 1: Simplificacion de gramaticas", styles["Heading2"]),
        Paragraph(
            "Se desarrollo un programa en Python que carga archivos de texto con "
            "producciones de una gramatica, valida cada linea con una expresion "
            "regular y elimina producciones epsilon.",
            styles["BodyText"],
        ),
        Spacer(1, 8),
        Paragraph("Validacion de producciones", styles["Heading3"]),
        Paragraph(
            "El programa acepta producciones con un no terminal en el lado izquierdo, "
            "una flecha -> o una flecha unicode, y una o mas alternativas separadas "
            "por el operador OR |. Si una linea no cumple el formato, la ejecucion se "
            "detiene e indica el numero de linea donde se encontro el error.",
            styles["BodyText"],
        ),
        Spacer(1, 8),
        Paragraph("Eliminacion de epsilon", styles["Heading3"]),
        Paragraph(
            "Primero se encuentran los simbolos anulables. Un simbolo es anulable si "
            "produce epsilon directamente o si todos los simbolos de alguno de sus "
            "cuerpos tambien son anulables. Despues, para cada produccion con m "
            "simbolos anulables, se generan los 2^m casos posibles conservando o "
            "eliminando dichos simbolos. Las producciones epsilon originales se "
            "remueven. Si el simbolo inicial es anulable, se agrega un nuevo simbolo "
            "inicial para conservar la capacidad de generar epsilon.",
            styles["BodyText"],
        ),
        Spacer(1, 8),
        Paragraph("Archivos incluidos", styles["Heading3"]),
        Paragraph(
            "El repositorio contiene el programa principal en src/grammar_simplifier.py "
            "y dos archivos de gramatica en la carpeta grammars. El README incluye "
            "instrucciones de ejecucion y un espacio para pegar el enlace del video "
            "no listado de YouTube.",
            styles["BodyText"],
        ),
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(OUTPUT), pagesize=letter)
    document.build(story)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
