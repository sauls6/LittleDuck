# Documentación del Proyecto Compilador LittleDuck

Este documento detalla el progreso y los entregables del proyecto de compilador para el lenguaje LittleDuck, dividido por entregas.

## Entrega 0: Diseño del Léxico

**Fecha de entrega:** 25 de abril

**Requisitos:**
1.  Diseñar las Expresiones Regulares que representan a los diferentes elementos de léxico.
2.  Listar todos los Tokens que serán reconocidos por el lenguaje.
3.  Generar un documento que contenga la definición de las expresiones regulares.

**Desarrollo:**

### 1. Expresiones Regulares y Tokens

Las expresiones regulares y los tokens para LittleDuck se definieron en el archivo de gramática de ANTLR (`LittleDuck.g4`). A continuación, se presentan los tokens y sus expresiones regulares correspondientes:

*   **Palabras Reservadas:**
    *   `PROGRAM`: `'program'`
    *   `MAIN`: `'main'`
    *   `END`: `'end'`
    *   `VAR`: `'var'`
    *   `INTTYPE`: `'int'`
    *   `FLTTYPE`: `'float'`
    *   `PRINT`: `'print'`
    *   `WHILE`: `'while'`
    *   `DO`: `'do'`
    *   `IF`: `'if'`
    *   `ELSE`: `'else'`
    *   `VOID`: `'void'`
*   **Delimitadores:**
    *   `SEMI`: `';'`
    *   `COMMA`: `','`
    *   `COLON`: `':'`
    *   `LBRACE`: `'{'`
    *   `RBRACE`: `'}'`
    *   `LPAREN`: `'('`
    *   `RPAREN`: `')'`
    *   `LBRACK`: `'['` (No utilizado actualmente en la gramática del parser)
    *   `RBRACK`: `']'` (No utilizado actualmente en la gramática del parser)
*   **Operadores:**
    *   `ASSIGN`: `'='`
    *   `EQUAL`: `'=='`
    *   `NOT_EQUAL`: `'!='`
    *   `GREATER`: `'>'`
    *   `LESS`: `'<'`
    *   `PLUS`: `'+'`
    *   `MINUS`: `'-'`
    *   `MULT`: `'*'`
    *   `DIV`: `'/'`
*   **Identificadores y Constantes:**
    *   `ID`: `[a-zA-Z] [a-zA-Z0-9_]*`
    *   `CTE_INT`: `[0-9]+`
    *   `CTE_FLOAT`: `[0-9]+ '.' [0-9]+`
    *   `CTE_STR`: `'"' (~["\n\r])* '"'`
*   **Espacios en Blanco y Saltos de Línea (Ignorados):**
    *   `WS`: `[ \t\r\n]+ -> skip`

Estos elementos se definieron directamente en el archivo `LittleDuck.g4`, que es utilizado por ANTLR para generar el analizador léxico.

### 2. Explicación de las Expresiones Regulares

A continuación, se explica el significado de las principales expresiones regulares definidas:

*   **`ID`**: `[a-zA-Z] [a-zA-Z0-9_]*`
    *   Un identificador comienza con una letra (mayúscula o minúscula) seguida de cero o más letras, dígitos o guiones bajos.
*   **`CTE_INT`**: `[0-9]+`
    *   Un entero es una secuencia de uno o más dígitos.
*   **`CTE_FLOAT`**: `[0-9]+ '.' [0-9]+`
    *   Un flotante es una secuencia de uno o más dígitos, seguido por un punto decimal y otra secuencia de uno o más dígitos.
*   **`CTE_STR`**: `'"' (~["\\n\\r])* '"'`
    *   Una cadena es cualquier secuencia de caracteres (excepto comillas dobles, saltos de línea y retornos de carro) encerrada entre comillas dobles.
*   **`WS`**: `[ \t\\r\\n]+ -> skip`
    *   Los espacios en blanco, tabulaciones, retornos de carro y saltos de línea son ignorados por el lexer.

## Entrega 1: Análisis Léxico

**Fecha de entrega:** 4 de mayo

**Requisitos:**
1.  Investigar herramientas de generación automática de compiladores.
2.  Seleccionar una herramienta adecuada.
3.  Desarrollar el Scanner (analizador léxico).
4.  Diseñar un Test-Plan y comprobar su funcionamiento.
5.  Documentar hallazgos, formato de reglas y expresiones regulares.

**Desarrollo:**

### 1. Herramientas de Generación de Compiladores
Se investigaron varias herramientas, y se seleccionó **ANTLR (ANother Tool for Language Recognition)**.
*   **Justificación de la Selección:** ANTLR es una potente herramienta generadora de parsers que puede construir analizadores léxicos, sintácticos, árboles de análisis y traductores a partir de una gramática. Es ampliamente utilizada, cuenta con buena documentación y se integra bien con Python, el lenguaje de desarrollo elegido para este proyecto.

### 2. Desarrollo del Scanner
El scanner (analizador léxico) se desarrolló utilizando ANTLR.
*   Las expresiones regulares definidas en la Entrega 0 se plasmaron en el archivo `LittleDuck.g4`.
*   ANTLR generó automáticamente el código del lexer en Python (`gen/LittleDuckLexer.py`) a partir de este archivo.
*   Se creó un script `lexer_runner.py` para probar el analizador léxico con archivos de entrada. Este script utiliza el lexer generado para tokenizar el código fuente y muestra los tokens encontrados, así como estadísticas y errores léxicos.

### 3. Test-Plan y Comprobación
Se diseñó un plan de pruebas para el analizador léxico, documentado en `docs/lexer_test_plan.md`.
*   Este plan incluye pruebas para tokens individuales, programas completos (mínimos, con variables, con estructuras de control) y programas con errores léxicos.
*   Los archivos de prueba se encuentran en el directorio `tests/lexer/` y `tests/lexer_tests.txt`.
*   El script `lexer_runner.py` se utilizó para ejecutar estas pruebas.

### 4. Documentación Adicional
*   **Formato de Reglas y Expresiones Regulares:** Las reglas léxicas (expresiones regulares) se definieron utilizando la sintaxis de ANTLR en el archivo `LittleDuck.g4`. Por ejemplo, `CTE_INT : [0-9]+ ;` define un token `CTE_INT` que corresponde a uno o más dígitos.

## Entrega 2: Análisis Sintáctico

**Fecha de entrega:** 11 de mayo

**Requisitos:**
1.  Desarrollar el Parser (analizador sintáctico) utilizando las reglas gramaticales y expresiones regulares.
2.  Diseñar un Test-Plan y comprobar su funcionamiento.
3.  Actualizar la documentación con el formato de las reglas gramaticales.

**Desarrollo:**

### 1. Desarrollo del Parser
El parser (analizador sintáctico) también se desarrolló utilizando ANTLR.
*   Las reglas gramaticales que definen la estructura del lenguaje LittleDuck se añadieron al archivo `LittleDuck.g4`, junto con las reglas léxicas.
    *   Ejemplo de regla gramatical: `program : PROGRAM ID SEMI vars? funcs? MAIN body END ;`
*   ANTLR generó automáticamente el código del parser en Python (`gen/LittleDuckParser.py`) y clases auxiliares como `gen/LittleDuckListener.py` y `gen/LittleDuckVisitor.py`.
*   Se creó un script `parser_runner.py` para probar el analizador sintáctico. Este script toma un archivo de entrada, lo procesa con el lexer y el parser, e informa si la sintaxis es correcta o si se encontraron errores. Opcionalmente, puede mostrar el árbol de análisis sintáctico y los tokens.

### 2. Test-Plan y Comprobación
Se diseñó un plan de pruebas para el analizador sintáctico, documentado en `docs/parser_test_plan.md`.
*   Este plan incluye pruebas para la estructura básica del programa, declaración de variables, funciones, statements (asignaciones, condicionales, ciclos, llamadas a función, print) y expresiones. También incluye pruebas para programas completos válidos y programas con diversos errores sintácticos.
*   Los archivos de prueba se encuentran en el directorio `tests/parser/` y se pueden ejecutar mediante `tests/parser_tests.bat` (o individualmente con `parser_runner.py`).

### 3. Documentación Adicional
*   **Formato de Reglas Gramaticales:** Las reglas gramaticales se definieron utilizando la sintaxis EBNF de ANTLR en el archivo `LittleDuck.g4`. Cada regla define un no terminal y la secuencia de terminales y otros no terminales que lo componen.
    *   Por ejemplo, la regla `statement : assignment | condition | cycle | f_call | print_stmt ;` define que un `statement` puede ser una `assignment`, una `condition`, etc.
    *   Los operadores como `?` (cero o uno), `*` (cero o más), y `+` (uno o más) se utilizan para especificar la cardinalidad.

---

## Entrega 3: Análisis Semántico

**Fecha de entrega:** (Por definir, según el avance del curso)

**Requisitos:**
1.  Diseñar la Tabla de consideraciones semánticas (cubo semántico) para el lenguaje.
2.  Implementar las estructuras de datos que representan al Directorio de Funciones y a las Tablas de Variables de LittleDuck.
3.  Establecer los puntos neurálgicos que permitan crear y llenar, tanto el Directorio de Funciones como las Tablas de variables del programa con las validaciones pertinentes.
4.  Agregar todo lo anterior a su Documentación: qué estructuras seleccionaron para cada situación (y porqué) así como cuáles son las principales operaciones.

**Desarrollo:**

### 1. Cubo Semántico (Tabla de Consideraciones Semánticas)

El cubo semántico define el tipo resultante de las operaciones binarias entre los tipos de datos del lenguaje LittleDuck (`INTTYPE`, `FLTTYPE`). También se considera un tipo `ERROR` para operaciones no válidas. Para los operadores relacionales, el resultado se considera `INTTYPE` (0 para falso, 1 para verdadero).

**Tipos de Datos Base:**
*   `INTTYPE`: Representa números enteros.
*   `FLTTYPE`: Representa números de punto flotante.
*   `VOID`: Usado para funciones que no retornan valor (no participa directamente en el cubo de operaciones binarias de expresiones).
*   `ERROR`: Indica una operación semánticamente incorrecta.

**Operadores Aritméticos:**

| Operador | Operando 1 | Operando 2 | Tipo Resultante |
| :------- | :--------- | :--------- | :-------------- |
| `+`      | `INTTYPE`  | `INTTYPE`  | `INTTYPE`       |
| `+`      | `INTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |
| `+`      | `FLTTYPE`  | `INTTYPE`  | `FLTTYPE`       |
| `+`      | `FLTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |
| `-`      | `INTTYPE`  | `INTTYPE`  | `INTTYPE`       |
| `-`      | `INTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |
| `-`      | `FLTTYPE`  | `INTTYPE`  | `FLTTYPE`       |
| `-`      | `FLTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |
| `*`      | `INTTYPE`  | `INTTYPE`  | `INTTYPE`       |
| `*`      | `INTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |
| `*`      | `FLTTYPE`  | `INTTYPE`  | `FLTTYPE`       |
| `*`      | `FLTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |
| `/`      | `INTTYPE`  | `INTTYPE`  | `FLTTYPE`       |
| `/`      | `INTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |
| `/`      | `FLTTYPE`  | `INTTYPE`  | `FLTTYPE`       |
| `/`      | `FLTTYPE`  | `FLTTYPE`  | `FLTTYPE`       |

**Operadores Relacionales:**
(Resultado `INTTYPE`: 0 para falso, 1 para verdadero)

| Operador             | Operando 1 | Operando 2 | Tipo Resultante |
| :------------------- | :--------- | :--------- | :-------------- |
| `<`, `>`, `==`, `!=` | `INTTYPE`  | `INTTYPE`  | `INTTYPE`       |
| `<`, `>`, `==`, `!=` | `INTTYPE`  | `FLTTYPE`  | `INTTYPE`       |
| `<`, `>`, `==`, `!=` | `FLTTYPE`  | `INTTYPE`  | `INTTYPE`       |
| `<`, `>`, `==`, `!=` | `FLTTYPE`  | `FLTTYPE`  | `INTTYPE`       |

**Operador de Asignación (`=`):**
(LHS = Lado Izquierdo, RHS = Lado Derecho)

| Operador | Tipo LHS  | Tipo RHS  | Tipo Resultante (del LHS) |
| :------- | :-------- | :-------- | :------------------------ |
| `=`      | `INTTYPE` | `INTTYPE` | `INTTYPE`                 |
| `=`      | `FLTTYPE` | `FLTTYPE` | `FLTTYPE`                 |
| `=`      | `FLTTYPE` | `INTTYPE` | `FLTTYPE` (Promoción)     |
| `=`      | `INTTYPE` | `FLTTYPE` | `ERROR` (Estrechamiento)  |

Cualquier otra combinación de tipos y operadores no listada explícitamente se considera un `ERROR`. Por ejemplo, `INTTYPE + VOID` sería `ERROR`.

Este documento se irá actualizando con las entregas subsecuentes del proyecto.
