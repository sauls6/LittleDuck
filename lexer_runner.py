"""
LittleDuck Lexer Runner
------------------------
Este script ejecuta el analizador léxico generado por ANTLR para tokenizar archivos
fuente escritos en el lenguaje LittleDuck.

Uso:
  python lexer_runner.py <archivo_entrada>
"""

import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from antlr4 import *
from gen.LittleDuckLexer import LittleDuckLexer
from antlr4.error.ErrorListener import ErrorListener


# Listener personalizado para errores léxicos
class LexicalErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Línea {line}:{column} - {msg}")

    def getErrorCount(self):
        return len(self.errors)

    def getErrors(self):
        return self.errors


def tokenize_file(input_file):
    """
    Analiza un archivo de entrada y muestra todos los tokens identificados.

    Args:
        input_file (str): Ruta al archivo que se va a analizar
    """
    print(f"Analizando archivo: {input_file}\n")

    # Crear un stream de caracteres a partir del archivo
    input_stream = FileStream(input_file, encoding='utf-8')

    # Crear el lexer
    lexer = LittleDuckLexer(input_stream)

    # Agregar listener personalizado para capturar errores léxicos
    error_listener = LexicalErrorListener()
    lexer.removeErrorListeners()  # Quitar los listeners por defecto
    lexer.addErrorListener(error_listener)

    # Obtener todos los tokens
    token_stream = CommonTokenStream(lexer)
    token_stream.fill()

    # Imprimir información de tokens
    print("TOKENS ENCONTRADOS:")
    print("-------------------")
    print(f"{'TOKEN':<12} {'TYPE':<8} {'LINE':<8} {'POS':<8} {'TEXT'}")
    print("-" * 70)

    # Contador para estadísticas
    token_count = 0
    token_types = {}

    for token in token_stream.tokens:
        # Ignorar el token EOF
        if token.type == Token.EOF:
            continue

        # Obtener el nombre del tipo de token
        token_type_name = lexer.symbolicNames[token.type]

        # Actualizar estadísticas
        token_count += 1
        token_types[token_type_name] = token_types.get(token_type_name, 0) + 1

        # Mostrar información del token
        print(f"{token_type_name:<12} {token.type:<8} {token.line:<8} {token.column:<8} '{token.text}'")

    # Mostrar estadísticas
    print("\nESTADÍSTICAS:")
    print(f"Total de tokens: {token_count}")
    print("Tokens por tipo:")
    for token_type, count in sorted(token_types.items()):
        print(f"  {token_type}: {count}")

    # Verificar si hubo errores léxicos
    if error_listener.getErrorCount() > 0:
        print("\nERRORES LÉXICOS DETECTADOS:")
        for err in error_listener.getErrors():
            print(" -", err)
    else:
        print("\nAnálisis léxico completado exitosamente. No se encontraron errores.")


def main():
    """
    Función principal que procesa argumentos de línea de comandos
    """
    if len(sys.argv) != 2:
        print("Uso: python lexer_runner.py <archivo_entrada>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: El archivo '{input_file}' no existe.")
        sys.exit(1)

    tokenize_file(input_file)


if __name__ == '__main__':
    main()
