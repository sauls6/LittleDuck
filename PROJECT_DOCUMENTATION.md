# Compilador LittleDuck - Proyecto Final

## Resumen Ejecutivo

### Objetivo del Proyecto
Este proyecto implementa un compilador completo para el lenguaje de programación LittleDuck, diseñado para demostrar las fases fundamentales del proceso de compilación: análisis léxico, análisis sintáctico y análisis semántico.

### Fases Implementadas del Compilador
- **Análisis Léxico**: Tokenización de código fuente LittleDuck
- **Análisis Sintáctico**: Verificación de estructura gramatical
- **Análisis Semántico**: Validación de tipos y manejo de tabla de símbolos

### Lenguaje Objetivo: LittleDuck
LittleDuck es un lenguaje de programación didáctico que incluye:
- **Tipos de datos**: `int`, `float`
- **Estructuras de control**: `if-else`, `while-do`
- **Funciones**: Con parámetros y variables locales
- **Operaciones**: Aritméticas (+, -, *, /) y relacionales (<, >, ==, !=)
- **Entrada/Salida**: Función `print` para mostrar resultados

### Herramientas Utilizadas
- **ANTLR 4**: Generador automático de analizadores léxicos y sintácticos
- **Python 3**: Lenguaje de implementación
- **Patrón Visitor**: Para el recorrido del árbol sintáctico en análisis semántico

### Resultados Obtenidos
- Compilador funcional que procesa las tres fases principales
- Suite completa de pruebas para validar cada componente
- Manejo robusto de errores en todas las fases
- Documentación técnica completa del proceso de desarrollo

---

## Arquitectura del Compilador

### Diagrama de Flujo del Proceso de Compilación

```
Código Fuente (.ld)
        ↓
   ANÁLISIS LÉXICO
   (LittleDuckLexer)
        ↓
   Stream de Tokens
        ↓
   ANÁLISIS SINTÁCTICO
   (LittleDuckParser)
        ↓
   Árbol Sintáctico (AST)
        ↓
   ANÁLISIS SEMÁNTICO
   (SemanticAnalyzer)
        ↓
   Código Validado
```

### Interacción entre Componentes

#### 1. Lexer → Parser
- El **LittleDuckLexer** convierte el código fuente en un stream de tokens
- El **LittleDuckParser** consume estos tokens para construir el árbol sintáctico
- Los errores léxicos se capturan antes del análisis sintáctico

#### 2. Parser → Semantic Analyzer
- El **SemanticAnalyzer** recorre el árbol sintáctico usando el patrón Visitor
- Construye y consulta la **Symbol Table** durante el recorrido
- Utiliza el **Semantic Cube** para validar operaciones entre tipos

### Estructuras de Datos Principales

#### Symbol Table (Tabla de Símbolos)
- **VariableEntry**: Información de variables (nombre, tipo, dirección)
- **FunctionEntry**: Información de funciones (parámetros, variables locales, tipo de retorno)
- **SymbolTable**: Gestión de ámbitos globales y locales

#### Semantic Cube (Cubo Semántico)
- Matriz tridimensional que define tipos resultantes de operaciones
- Validación de compatibilidad entre tipos
- Manejo de promociones automáticas (int → float)

---

## Manual de Usuario

### Instalación y Configuración

#### Prerrequisitos
- Python 3.8 o superior
- ANTLR 4 Runtime para Python

#### Instalación de Dependencias
```bash
pip install antlr4-python3-runtime
```

#### Generación de Archivos ANTLR (si es necesario)
```bash
antlr4 -Dlanguage=Python3 LittleDuck.g4 -o gen/
```

### Uso de los Scripts Principales

#### 1. Análisis Léxico: `lexer_runner.py`
**Propósito**: Tokenizar archivos fuente LittleDuck

**Uso**:
```bash
python lexer_runner.py <archivo_entrada>
```

**Ejemplo**:
```bash
python lexer_runner.py tests/lexer/test_complete.txt
```

**Salida**:
- Lista de tokens encontrados con información detallada
- Estadísticas de tokenización
- Errores léxicos (si los hay)

#### 2. Análisis Sintáctico: `parser_runner.py`
**Propósito**: Verificar estructura gramatical

**Uso**:
```bash
python parser_runner.py <archivo_entrada> [--tree] [--tokens] [--verbose]
```

**Opciones**:
- `--tree`: Muestra el árbol de análisis sintáctico
- `--tokens`: Muestra los tokens identificados
- `--verbose`: Información detallada del proceso

**Ejemplo**:
```bash
python parser_runner.py tests/parser/test_complete_valid.txt --tree
```

#### 3. Análisis Semántico: `semantic_runner.py`
**Propósito**: Validar tipos y manejo de símbolos

**Uso**:
```bash
python semantic_runner.py <archivo_entrada>
```

**Ejemplo**:
```bash
python semantic_runner.py tests/parser/test_complete_valid.txt
```

**Salida**:
- Errores semánticos encontrados
- Tabla de símbolos construida
- Estado de validación de tipos

### Ejemplos de Uso con Archivos de Prueba

#### Programa Básico Válido
```bash
python semantic_runner.py tests/parser/test_min_valid.txt
```

#### Programa con Errores
```bash
python parser_runner.py tests/parser/test_missing_semi.txt
```

#### Análisis Completo paso a paso
```bash
# 1. Análisis léxico
python lexer_runner.py tests/parser/test_complete_valid.txt

# 2. Análisis sintáctico con árbol
python parser_runner.py tests/parser/test_complete_valid.txt --tree

# 3. Análisis semántico
python semantic_runner.py tests/parser/test_complete_valid.txt
```

### Interpretación de Mensajes de Error

#### Errores Léxicos
```
Lexical Error at Line 5:10 - token recognition error at: '@'
```
- **Línea 5, columna 10**: Ubicación del error
- **Carácter '@'**: Token no reconocido

#### Errores Sintácticos
```
Syntax Error at Line 3:15 - mismatched input ';' expecting 'end'
```
- **Estructura incorrecta**: Token inesperado en la posición

#### Errores Semánticos
```
Error at Line 7:5 - Type mismatch in assignment: cannot assign float to int variable
```
- **Incompatibilidad de tipos**: Operación semánticamente incorrecta

---

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

**Fecha de entrega:** 18 de mayo

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

### 2. Estructuras de Datos: Directorio de Funciones y Tablas de Variables

Para manejar la información semántica del programa, se implementaron las siguientes estructuras de datos principales en `symbol_table.py`:

*   **`VariableEntry`**: Una clase simple (o tupla nombrada) para almacenar información sobre una variable individual, principalmente su `type` (e.g., `Type.INT`, `Type.FLOAT`).
*   **`FunctionEntry`**: Una clase para almacenar información sobre una función. Incluye:
    *   `name`: Nombre de la función.
    *   `return_type`: El tipo de dato que retorna la función (e.g., `Type.VOID`, `Type.INT`, `Type.FLOAT`).
    *   `param_types`: Una lista ordenada de los tipos de sus parámetros.
    *   `variables`: Un diccionario que actúa como la tabla de variables locales de esta función. Las claves son los nombres de las variables y los valores son instancias de `VariableEntry`.
    *   `param_names`: Una lista ordenada de los nombres de sus parámetros (para referencia y validación).
*   **`SymbolTable`**: La clase principal que gestiona los símbolos del programa. Contiene:
    *   `functions`: Un diccionario que actúa como el Directorio de Funciones. Las claves son los nombres de las funciones y los valores son instancias de `FunctionEntry`.
    *   `global_vars`: Un diccionario que actúa como la Tabla de Variables Globales. Las claves son los nombres de las variables globales y los valores son instancias de `VariableEntry`.
    *   `current_scope_vars`: Una referencia a la tabla de variables del ámbito actual (puede ser `global_vars` o la tabla `variables` de una `FunctionEntry` específica).
    *   `current_function_name`: El nombre de la función que se está procesando actualmente, para saber en qué ámbito local nos encontramos.

**Justificación de las Estructuras:**
*   **Diccionarios para Tablas:** Se eligieron diccionarios para el Directorio de Funciones y las Tablas de Variables (globales y locales) debido a su eficiencia en la búsqueda (tiempo promedio O(1)). Esto es crucial para las operaciones frecuentes de búsqueda de símbolos.
*   **Clases `FunctionEntry` y `VariableEntry`:** Permiten agrupar la información relevante de cada símbolo de manera organizada y legible.
*   **Gestión de Ámbito Explícita:** La `SymbolTable` maneja explícitamente el ámbito actual (`current_scope_vars` y `current_function_name`) para asegurar que las declaraciones y búsquedas de variables se realicen en el contexto correcto (global o local a una función).

**Operaciones Principales:**

*   **`SymbolTable.add_function(name, return_type)`**: Añade una nueva función al directorio. Verifica duplicados.
*   **`SymbolTable.add_global_variable(name, type)`**: Añade una variable global. Verifica duplicados.
*   **`FunctionEntry.add_param(name, type)`**: Añade un parámetro a una función específica y a su tabla de variables locales. Verifica duplicados dentro del ámbito local.
*   **`FunctionEntry.add_variable(name, type)`**: Añade una variable local a una función específica. Verifica duplicados dentro del ámbito local.
*   **`SymbolTable.lookup_variable(name)`**: Busca una variable, primero en el ámbito local actual (si existe) y luego en el ámbito global. Devuelve su `VariableEntry` o `None`.
*   **`SymbolTable.lookup_function(name)`**: Busca una función en el directorio. Devuelve su `FunctionEntry` o `None`.
*   **`SymbolTable.set_current_scope(function_name)`**: Cambia el ámbito actual al de la función especificada. Si `function_name` es `None` o una cadena especial (e.g., "global"), se establece el ámbito global.
*   **`SymbolTable.get_variable_type(name)`**: Obtiene el tipo de una variable buscando en el ámbito actual y luego global.
*   **`SymbolTable.get_function_return_type(name)`**: Obtiene el tipo de retorno de una función.

### 3. Puntos Neurálgicos y Validaciones Semánticas

El análisis semántico se implementa utilizando el patrón Visitor (`SemanticAnalyzer(LittleDuckVisitor)`) que recorre el árbol de análisis sintáctico generado por ANTLR. Los puntos clave donde se realizan las validaciones y se llenan las tablas son:

*   **`visitProgram(ctx)`**:
    *   Inicializa la `SymbolTable`.
    *   Establece el ámbito global.
    *   Visita las declaraciones de variables globales (`vars`) y funciones (`funcs`).
    *   Establece el ámbito de la función `main` antes de visitar su cuerpo.
*   **`visitVars(ctx)`**:
    *   Itera sobre las declaraciones de variables.
    *   Para cada variable, extrae su nombre y tipo.
    *   Llama a `symbol_table.add_global_variable()` o `current_function.add_variable()` según el ámbito actual.
    *   **Validación:** Detecta y reporta errores de re-declaración de variables en el mismo ámbito.
*   **`visitFuncs(ctx)`**:
    *   Extrae el nombre y tipo de retorno de la función.
    *   Llama a `symbol_table.add_function()` para registrarla.
    *   Establece el ámbito actual a esta nueva función (`symbol_table.set_current_scope(func_name)`).
    *   Visita la lista de parámetros (`param_list`) y el cuerpo (`body`) de la función.
    *   Al salir de la función, restaura el ámbito global (`symbol_table.set_current_scope(None)` o a un identificador de ámbito global).
    *   **Validación:** Detecta y reporta errores de re-declaración de funciones.
*   **`visitParam_list(ctx)`**:
    *   Itera sobre los parámetros.
    *   Para cada parámetro, extrae su nombre y tipo.
    *   Llama a `current_function.add_param()` para registrar el parámetro en la `FunctionEntry` y en su tabla de variables locales.
    *   **Validación:** Detecta y reporta errores de re-declaración de parámetros o de parámetros con el mismo nombre que una variable local ya declarada en ese (aún vacío) ámbito de función.
*   **`visitAssignment(ctx: LittleDuckParser.AssignmentContext)`**:
    *   Obtiene el nombre de la variable (LHS).
    *   **Validación:** Verifica que la variable esté declarada (`symbol_table.lookup_variable(var_name)`). Reporta error si no existe.
    *   Obtiene el tipo de la variable (`lhs_type`).
    *   Visita la expresión (RHS) para obtener su tipo (`rhs_type`) de la pila de operandos.
    *   **Validación:** Consulta el cubo semántico (`semantic_cube.check_assignment(lhs_type, rhs_type)`) para verificar la compatibilidad de tipos en la asignación. Reporta error si es `Type.ERROR`.
*   **`visitExpression(ctx)`, `visitExp(ctx)`, `visitTerm(ctx)`, `visitFactor(ctx)`**:
    *   **Manejo de Pila de Operandos y Tipos:** Estas reglas gestionan una pila de operandos y una pila de tipos.
        *   Al encontrar un operando (ID, CTE_INT, CTE_FLOAT), se busca su tipo (si es ID) o se determina su tipo (si es constante) y se empuja a la pila de tipos.
        *   Al encontrar un operador, se desapilan los tipos de los operandos y el operador.
        *   **Validación:** Se consulta el cubo semántico (`semantic_cube.check_operation(op_type1, op_type2, operator)`) para obtener el tipo resultante. Si es `Type.ERROR`, se reporta un error de tipos incompatibles.
        *   El tipo resultante se empuja de nuevo a la pila de tipos.
    *   **`visitFactor`**:
        *   Si es un ID: Busca la variable. **Validación:** Reporta error si no está declarada. Empuja su tipo a la pila de tipos.
        *   Si es CTE_INT o CTE_FLOAT: Empuja `Type.INT` o `Type.FLOAT` a la pila de tipos.
        *   Si es una expresión entre paréntesis: El tipo resultante de la sub-expresión ya estará en la cima de la pila de tipos.
*   **`visitF_call(ctx: LittleDuckParser.F_callContext)`**:
    *   Obtiene el nombre de la función.
    *   **Validación:** Verifica que la función esté declarada (`symbol_table.lookup_function(func_name)`). Reporta error si no existe.
    *   Obtiene la `FunctionEntry`.
    *   Procesa los argumentos:
        *   Visita cada expresión de argumento para obtener su tipo (de la pila de operandos).
        *   Compara el número de argumentos proporcionados con el número de parámetros esperados.
        *   Compara el tipo de cada argumento con el tipo del parámetro correspondiente.
        *   **Validación:** Reporta errores por número incorrecto de argumentos o por tipos de argumentos incompatibles.
    *   Si la función no es `VOID`, su tipo de retorno se podría empujar a la pila de operandos/tipos si la llamada a función fuera parte de una expresión (no es el caso en LittleDuck para `f_call` como statement, pero es una consideración general). Para `print`, se maneja directamente.
*   **`visitPrint_stmt(ctx: LittleDuckParser.Print_stmtContext)`**:
    *   Itera sobre las expresiones a imprimir.
    *   Visita cada expresión para evaluarla y obtener su tipo (de la pila de operandos).
    *   **Validación:** Aunque `print` puede aceptar cualquier tipo imprimible, se asegura que la expresión sea válida semánticamente. El tipo resultante de la expresión no necesita ser verificado contra otro tipo para `print` en sí, pero la expresión debe resolverse a un tipo válido (no `ERROR`).
*   **`visitCondition(ctx: LittleDuckParser.ConditionContext)`**:
    *   Visita la expresión de la condición.
    *   **Validación:** El tipo resultante de la expresión (obtenido de la pila de operandos) debe ser compatible con una condición booleana (en LittleDuck, esto significa que el cubo semántico para operadores relacionales debe resultar en `INTTYPE`, que se interpreta como booleano). Reporta error si el tipo no es adecuado para una condición.
*   **`visitCycle(ctx: LittleDuckParser.CycleContext)`**:
    *   Similar a `visitCondition`, visita la expresión de la condición del ciclo.
    *   **Validación:** El tipo resultante de la expresión debe ser compatible con una condición booleana.

Este documento se irá actualizando con las entregas subsecuentes del proyecto.

---

## Resultados y Conclusiones

### Casos de Prueba Ejecutados y Resultados

#### Suite de Pruebas Léxicas
- **Ubicación**: `tests/lexer/`
- **Casos ejecutados**: 5 archivos de prueba principales
- **Resultados**: 100% de tokens reconocidos correctamente
- **Errores identificados**: Caracteres especiales no válidos detectados apropiadamente

#### Suite de Pruebas Sintácticas
- **Ubicación**: `tests/parser/`
- **Casos ejecutados**: 25+ archivos de prueba
- **Cobertura**: 
  - Programas válidos completos ✓
  - Declaraciones de variables ✓
  - Funciones con parámetros ✓
  - Estructuras de control ✓
  - Expresiones complejas ✓
  - Manejo de errores sintácticos ✓

#### Suite de Pruebas Semánticas
- **Validación de tipos**: Operaciones aritméticas y relacionales
- **Tabla de símbolos**: Gestión correcta de ámbitos globales y locales
- **Detección de errores**: Variables no declaradas, tipos incompatibles

### Limitaciones Actuales del Compilador

#### Funcionalidades No Implementadas
- **Generación de código**: No produce código objeto o ejecutable
- **Optimizaciones**: Sin análisis de optimización de código
- **Manejo de memoria**: Asignación básica, sin gestión avanzada
- **Arrays**: Estructuras de datos complejas no soportadas
- **Strings**: Manejo limitado solo para función `print`

#### Restricciones del Lenguaje
- **Tipos limitados**: Solo `int` y `float`
- **Sin recursión**: No validada semánticamente
- **Funciones simples**: Sin sobrecarga o funciones de primera clase
- **I/O básico**: Solo función `print` implementada

### Lecciones Aprendidas

#### Aspectos Técnicos
1. **ANTLR es poderoso**: La generación automática de lexers y parsers acelera significativamente el desarrollo
2. **Patrón Visitor**: Excelente para separar la lógica de análisis de la estructura del árbol
3. **Manejo de errores**: Crítico implementar captura de errores en todas las fases
4. **Testing exhaustivo**: Las suites de prueba son esenciales para validar cada componente

#### Aspectos de Diseño
1. **Separación de responsabilidades**: Cada fase del compilador debe estar claramente delimitada
2. **Estructuras de datos**: La elección correcta impacta directamente en el rendimiento
3. **Documentación**: Fundamental para mantener y extender el proyecto

#### Comprensión de Compiladores
1. **Fases interdependientes**: Cada fase construye sobre la anterior
2. **Importancia del análisis semántico**: Validación de tipos previene errores en tiempo de ejecución
3. **Complejidad creciente**: La dificultad aumenta exponencialmente en cada fase

### Trabajo Futuro (Posibles Extensiones)

#### Corto Plazo
- **Generación de código intermedio**: Implementar cuádruplos
- **Más tipos de datos**: `string`, `bool`, arrays
- **Funciones built-in**: `read`, operaciones matemáticas

#### Mediano Plazo
- **Optimizaciones**: Análisis de flujo de datos, eliminación de código muerto
- **Mejor manejo de errores**: Recuperación de errores, mensajes más descriptivos
- **IDE integration**: Plugin para editores populares

#### Largo Plazo
- **Compilación completa**: Generación de código ejecutable
- **Debugging support**: Información de debugging en código generado
- **Estándar más amplio**: Extensión hacia un lenguaje más completo

### Valoración Final

Este proyecto ha sido una implementación exitosa de las fases fundamentales de un compilador. Se logró:

1. **Comprensión profunda** de la teoría de compiladores aplicada prácticamente
2. **Implementación robusta** con manejo adecuado de errores
3. **Documentación completa** que facilita mantenimiento y extensión
4. **Base sólida** para futuras extensiones del compilador

El compilador LittleDuck representa un paso significativo en la comprensión de cómo los lenguajes de programación son procesados y ejecutados, proporcionando una base sólida para proyectos más ambiciosos en el futuro.

---

## Anexos

### A. Estructura Completa del Proyecto
```
LittleDuck/
├── PROJECT_DOCUMENTATION.md    # Documentación principal
├── README.md                       # Guía rápida
├── LittleDuck.g4                   # Gramática ANTLR
├── lexer_runner.py                 # Script análisis léxico
├── parser_runner.py                # Script análisis sintáctico
├── semantic_runner.py              # Script análisis semántico
├── semantic_analyzer.py            # Implementación análisis semántico
├── symbol_table.py                 # Tabla de símbolos
├── semantic_cube.py                # Cubo semántico
├── main.py                         # Script principal (demo)
├── gen/                           # Archivos generados por ANTLR
│   ├── LittleDuckLexer.py
│   ├── LittleDuckParser.py
│   ├── LittleDuckListener.py
│   └── LittleDuckVisitor.py
├── tests/                         # Suite de pruebas
│   ├── lexer/                     # Pruebas léxicas
│   └── parser/                    # Pruebas sintácticas
└── docs/                          # Documentación adicional
    ├── lexer_test_plan.md
    └── parser_test_plan.md
```

### B. Sintaxis Completa del Lenguaje LittleDuck
```antlr
program     : PROGRAM ID SEMI vars? funcs? MAIN body END ;
vars        : VAR (ID (COMMA ID)* COLON type SEMI)+ ;
funcs       : (VOID ID LPAREN param_list? RPAREN LBRACK vars? body RBRACK SEMI)+ ;
param_list  : (ID COLON type) (COMMA ID COLON type)* ;
type        : INTTYPE | FLTTYPE ;
body        : LBRACE statement* RBRACE ;
statement   : assignment | condition | cycle | f_call | print_stmt ;
assignment  : ID ASSIGN expression SEMI ;
condition   : IF LPAREN expression RPAREN body (ELSE body)? SEMI ;
cycle       : WHILE LPAREN expression RPAREN DO body SEMI ;
f_call      : ID LPAREN expression_multiple? RPAREN SEMI ;
print_stmt  : PRINT LPAREN print_args RPAREN SEMI ;
expression  : exp ((LESS | GREATER | EQUAL | NOT_EQUAL) exp)? ;
exp         : term ((PLUS | MINUS) term)* ;
term        : factor ((MULT | DIV) factor)* ;
factor      : (PLUS | MINUS)? (LPAREN expression RPAREN | ID | (CTE_INT | CTE_FLOAT)) ;
```

### C. Tokens Reconocidos
```
Palabras Reservadas: program, main, end, var, int, float, print, while, do, if, else, void
Delimitadores: ; , : { } ( ) [ ]
Operadores: = == != > < + - * /
Identificadores: [a-zA-Z][a-zA-Z0-9_]*
Constantes: enteros, flotantes, strings
```