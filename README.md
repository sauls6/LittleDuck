# Compilador LittleDuck

Un compilador completo para el lenguaje de programación LittleDuck, implementando las fases de análisis léxico, sintáctico y semántico.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8 o superior
- ANTLR 4 Runtime para Python

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd LittleDuck

# Instalar dependencias
pip install antlr4-python3-runtime

# Generar archivos ANTLR (si es necesario)
antlr4 -Dlanguage=Python3 LittleDuck.g4 -o gen/
```

### Uso Básico
```bash
# Análisis léxico
python lexer_runner.py tests/parser/test_complete_valid.txt

# Análisis sintáctico
python parser_runner.py tests/parser/test_complete_valid.txt --tree

# Análisis semántico completo
python semantic_runner.py tests/parser/test_complete_valid.txt
```

## 📋 Características

### Lenguaje LittleDuck Soportado
- **Tipos de datos**: `int`, `float`
- **Variables**: Globales y locales con alcance de función
- **Funciones**: Con parámetros y variables locales
- **Estructuras de control**: `if-else`, `while-do`
- **Operadores**: 
  - Aritméticos: `+`, `-`, `*`, `/`
  - Relacionales: `<`, `>`, `==`, `!=`
  - Asignación: `=`
- **I/O**: Función `print` para salida

### Fases del Compilador Implementadas
- ✅ **Análisis Léxico**: Tokenización completa
- ✅ **Análisis Sintáctico**: Verificación gramatical
- ✅ **Análisis Semántico**: Validación de tipos y símbolos
- ❌ **Generación de Código**: No implementado

## 🛠️ Herramientas y Scripts

### Scripts Principales

| Script | Propósito | Uso |
|--------|-----------|-----|
| `lexer_runner.py` | Análisis léxico | `python lexer_runner.py <archivo>` |
| `parser_runner.py` | Análisis sintáctico | `python parser_runner.py <archivo> [opciones]` |
| `semantic_runner.py` | Análisis semántico | `python semantic_runner.py <archivo>` |

### Opciones de Parser
- `--tree`: Muestra árbol sintáctico
- `--tokens`: Lista tokens encontrados
- `--verbose`: Información detallada

## 📁 Estructura del Proyecto

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
├── gen/                            # Archivos generados por ANTLR
├── tests/                          # Suite de pruebas
└── docs/                           # Documentación adicional
```

## 🧪 Ejemplos y Pruebas

### Programa LittleDuck Básico
```
program ejemplo;
var x, y : int;
main {
    x = 5;
    y = x + 3;
    print(x, y);
}
end
```

### Ejecutar Pruebas
```bash
# Todas las pruebas léxicas
python lexer_runner.py tests/lexer/test_complete.txt

# Pruebas sintácticas con diferentes casos
python parser_runner.py tests/parser/test_complete_valid.txt
python parser_runner.py tests/parser/test_missing_semi.txt

# Análisis semántico
python semantic_runner.py tests/parser/test_complete_valid.txt
```

### Casos de Prueba Disponibles
- **Léxicos**: `tests/lexer/` - Tokens válidos e inválidos
- **Sintácticos**: `tests/parser/` - Programas válidos y con errores
- **Semánticos**: Validación usando archivos del parser

## 🔍 Interpretación de Resultados

### Análisis Exitoso
```
Lexical and Syntax analysis successful.
--- Starting Semantic Analysis ---
--- Finished Semantic Analysis ---
--- Symbol Table ---
[Tabla de símbolos generada]
```

### Errores Comunes
```bash
# Error léxico
Lexical Error at Line 5:10 - token recognition error at: '@'

# Error sintáctico  
Syntax Error at Line 3:15 - mismatched input ';' expecting 'end'

# Error semántico
Error at Line 7:5 - Type mismatch: cannot assign float to int variable
```

## 🏗️ Arquitectura Técnica

### Componentes Principales
- **LittleDuckLexer**: Generado por ANTLR, tokeniza código fuente
- **LittleDuckParser**: Generado por ANTLR, construye AST
- **SemanticAnalyzer**: Visitor pattern para análisis semántico
- **SymbolTable**: Gestión de ámbitos y declaraciones
- **SemanticCube**: Validación de operaciones entre tipos

### Flujo de Compilación
```
Código Fuente → Lexer → Tokens → Parser → AST → Semantic Analyzer → Código Validado
```

## 📚 Documentación Completa

Para información detallada sobre:
- Diseño del compilador
- Especificación completa del lenguaje
- Arquitectura técnica
- Manual de usuario avanzado
- Resultados y conclusiones

Consulta: **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)**

## 📋 Estado del Proyecto

### Entregas Completadas
- [x] **Entrega 0**: Diseño del Léxico
- [x] **Entrega 1**: Análisis Léxico  
- [x] **Entrega 2**: Análisis Sintáctico
- [x] **Entrega 3**: Análisis Semántico
- [x] **Entrega Final**: Documentación general

## En este proyecto aprendí:
- Teoría de lenguajes formales: Desde básicos como gramáticas hasta temas como autómatas y expresiones regulares implementados en ANTLR, así como teoría de cuadruplas y cubos semánticos.
- Análisis léxico y sintáctico: Implementación de un lexer y parser completos para el lenguaje LittleDuck.
- Análisis semántico y tipos: Validación de tipos y gestión de símbolos.
- Gestión de tabla de símbolos: Manejo de variables y funciones con su respectivo scope.
- Herramientas de desarrollo (ANTLR): Entendimiento de los archivos generados gracias a las clases teóricas y su uso en Python al hacer el compilador.
- Testing y validación de compiladores: Personalmente me enfoqué en el desarrollo de este proyecto intentando en todo momento tener un framwork sencillo pero robusto para pruebas, lo que me permitió validar cada fase del compilador de manera efectiva.

**Autor**: Saúl Sánchez Rangel - Ingeniero en Tecnologías Computacionales  
**Herramientas**: ANTLR 4, Python 3  
**Licencia**: Ver [LICENSE](LICENSE)
