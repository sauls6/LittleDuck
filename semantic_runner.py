# semantic_runner.py
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from antlr4 import *
from gen.LittleDuckLexer import LittleDuckLexer
from gen.LittleDuckParser import LittleDuckParser
from semantic_analyzer import SemanticAnalyzer
from symbol_table import SymbolTable
from semantic_cube import SemanticCube
from antlr4.error.ErrorListener import ErrorListener

class LexerErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Lexical Error at Line {line}:{column} - {msg}")

    def get_errors(self):
        return self.errors

class ParserErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Syntax Error at Line {line}:{column} - {msg}")

    def get_errors(self):
        return self.errors

def main(argv):
    if len(argv) < 2:
        print("Usage: python semantic_runner.py <input_file>")
        return

    input_file = argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    print(f"Analyzing file: {input_file}\n")
    input_stream = FileStream(input_file, encoding='utf-8')

    # Lexer
    lexer = LittleDuckLexer(input_stream)
    lexer_error_listener = LexerErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexer_error_listener)
    stream = CommonTokenStream(lexer)

    # Parser
    parser = LittleDuckParser(stream)
    parser_error_listener = ParserErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(parser_error_listener)
    tree = parser.program() # Start parsing from the 'program' rule

    lex_errors = lexer_error_listener.get_errors()
    par_errors = parser_error_listener.get_errors()

    if lex_errors:
        print("Lexical Errors Found:")
        for err in lex_errors:
            print(err)
        # Optionally, stop if lexical errors are present
        # return

    if par_errors:
        print("Syntax Errors Found:")
        for err in par_errors:
            print(err)
        # Stop if syntax errors are present, as semantic analysis might be unreliable
        return 
    
    if not lex_errors and not par_errors:
        print("Lexical and Syntax analysis successful.\n")
        # Semantic Analysis
        symbol_table = SymbolTable()
        semantic_cube = SemanticCube()
        analyzer = SemanticAnalyzer(symbol_table, semantic_cube)
        
        print("--- Starting Semantic Analysis ---")
        semantic_errors = analyzer.visit(tree) # Use the generic visit method for the visitor
        print("--- Finished Semantic Analysis ---")

        print("\n--- Symbol Table ---")
        print(symbol_table)
        print("--------------------\n")

        if semantic_errors:
            print("Semantic Errors Found:")
            for err in semantic_errors:
                print(err)
        else:
            print("Semantic analysis successful. No errors found.")
    else:
        print("Compilation failed due to lexical or syntax errors.")

if __name__ == '__main__':
    main(sys.argv)
