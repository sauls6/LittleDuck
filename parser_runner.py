"""
LittleDuck Parser Runner
------------------------
Este script ejecuta el analizador sintáctico generado por ANTLR para verificar
la estructura gramatical de archivos fuente escritos en el lenguaje LittleDuck.

Uso:
  python parser_runner.py <archivo_entrada> [--tree] [--tokens] [--verbose]

Opciones:
  --tree    : Muestra el árbol de análisis sintáctico
  --tokens  : Muestra los tokens identificados
  --verbose : Muestra información detallada del proceso de análisis
"""

import sys
import os

import antlr4
from antlr4 import *
from gen.LittleDuckLexer import LittleDuckLexer
from gen.LittleDuckParser import LittleDuckParser
from gen.LittleDuckListener import LittleDuckListener


class ErrorListener(antlr4.DiagnosticErrorListener):
    """
    Clase personalizada para escuchar y reportar errores durante el análisis.
    """

    def __init__(self, verbose=False):
        super().__init__()
        self.errors = []
        self.verbose = verbose

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_message = f"Error sintáctico en línea {line}:{column} - {msg}"
        self.errors.append(error_message)
        if self.verbose:
            print(error_message)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        if self.verbose:
            message = f"Ambigüedad detectada entre índices {startIndex} y {stopIndex}"
            print(message)

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        if self.verbose:
            message = f"Intentando análisis con contexto completo entre índices {startIndex} y {stopIndex}"
            print(message)

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        if self.verbose:
            message = f"Sensibilidad de contexto detectada entre índices {startIndex} y {stopIndex}"
            print(message)


class LittleDuckTreeListener(LittleDuckListener):
    """
    Listener para rastrear el recorrido del árbol sintáctico.
    """

    def __init__(self, parser):
        self.parser = parser
        self.depth = 0

    def enterEveryRule(self, ctx):
        rule_name = self.parser.ruleNames[ctx.getRuleIndex()]
        print("  " * self.depth + f"► {rule_name}")
        self.depth += 1

    def exitEveryRule(self, ctx):
        self.depth -= 1


def parse_file(input_file, show_tree=False, show_tokens=False, verbose=False):
    """
    Analiza un archivo de entrada utilizando el parser de LittleDuck.
    Toma:
        input_file (str): Ruta al archivo que se va a analizar
        show_tree (bool): Si es True, muestra el árbol sintáctico
        show_tokens (bool): Si es True, muestra los tokens
        verbose (bool): Si es True, muestra información adicional durante el análisis
    """
    print(f"Analizando sintácticamente el archivo: {input_file}\n")

    # Crear un stream de caracteres a partir del archivo
    input_stream = FileStream(input_file, encoding='utf-8')

    # Crear el lexer
    lexer = LittleDuckLexer(input_stream)

    # Configurar el listener de errores para el lexer
    lexer_error_listener = ErrorListener(verbose)
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexer_error_listener)

    # Obtener el stream de tokens
    token_stream = CommonTokenStream(lexer)

    # Mostrar los tokens si se solicita
    if show_tokens:
        token_stream.fill()
        print("TOKENS ENCONTRADOS:")
        print("-------------------")
        print(f"{'TOKEN':<12} {'TYPE':<8} {'LINE':<8} {'POS':<8} {'TEXT'}")
        print("-" * 70)

        for token in token_stream.tokens:
            if token.type == Token.EOF:
                continue

            token_type_name = lexer.symbolicNames[token.type]
            print(f"{token_type_name:<12} {token.type:<8} {token.line:<8} {token.column:<8} '{token.text}'")

        print("\n")

        # Reset token stream para el parser
        token_stream = CommonTokenStream(lexer)

    # Crear el parser
    parser = LittleDuckParser(token_stream)

    # Configurar el listener de errores para el parser
    parser_error_listener = ErrorListener(verbose)
    parser.removeErrorListeners()
    parser.addErrorListener(parser_error_listener)

    # Activar SLL para mejor rendimiento (puede cambiarse a LL si hay problemas)
    parser._interp.predictionMode = PredictionMode.SLL

    try:
        # Comenzar el análisis desde la regla 'program'
        tree = parser.program()

        # Mostrar estadísticas
        print("\nESTADÍSTICAS DE ANÁLISIS SINTÁCTICO:")
        print(f"Número de errores sintácticos: {len(parser_error_listener.errors)}")

        # Mostrar el árbol si se solicita
        if show_tree and len(parser_error_listener.errors) == 0:
            print("\nÁRBOL SINTÁCTICO:")
            print("-----------------")
            listener = LittleDuckTreeListener(parser)
            walker = ParseTreeWalker()
            walker.walk(listener, tree)

        # Verificar si hubo errores
        if len(parser_error_listener.errors) > 0:
            print("\nERRORES SINTÁCTICOS DETECTADOS:")
            for error in parser_error_listener.errors:
                print(f"  • {error}")
            return False
        else:
            print("\nAnálisis sintáctico completado exitosamente. No se encontraron errores.")
            return True

    except Exception as e:
        print(f"\nERROR INESPERADO: {str(e)}")
        return False


def main():
    """
    Función principal que procesa argumentos de línea de comandos
    """
    if len(sys.argv) < 2:
        print("Uso: python parser_runner.py <archivo_entrada> [--tree] [--tokens] [--verbose]")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: El archivo '{input_file}' no existe.")
        sys.exit(1)

    show_tree = "--tree" in sys.argv
    show_tokens = "--tokens" in sys.argv
    verbose = "--verbose" in sys.argv

    success = parse_file(input_file, show_tree, show_tokens, verbose)

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()