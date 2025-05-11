# Test Plan para el Analizador Sintáctico de LittleDuck

## 1. Objetivos de las Pruebas

El objetivo principal de este test plan es verificar que el analizador sintáctico desarrollado pueda:

1. Reconocer la estructura correcta de programas escritos en LittleDuck
2. Detectar errores sintácticos en programas incorrectos
3. Generar árboles de análisis sintáctico acordes a la gramática definida
4. Manejar todos los elementos sintácticos del lenguaje LittleDuck

## 2. Casos de Prueba

### 2.1. Pruebas de Estructura Básica del Programa

| ID | Descripción | Archivo | Resultado Esperado |
|----|-------------|---------|-------------------|
| P01 | Programa mínimo válido | `test_min_valid.txt` | Análisis exitoso, sin errores |
| P02 | Programa sin la palabra clave 'program' | `test_missing_program.txt` | Error sintáctico |
| P03 | Programa sin punto y coma después del ID | `test_missing_semi.txt` | Error sintáctico |
| P04 | Programa sin la palabra clave 'main' | `test_missing_main.txt` | Error sintáctico |
| P05 | Programa sin la palabra clave 'end' | `test_missing_end.txt` | Error sintáctico |

### 2.2. Pruebas de Declaración de Variables

| ID | Descripción | Archivo | Resultado Esperado |
|----|-------------|---------|-------------------|
| V01 | Declaración simple de variables | `test_vars_simple.txt` | Análisis exitoso, sin errores |
| V02 | Declaración múltiple de variables | `test_vars_multiple.txt` | Análisis exitoso, sin errores |
| V03 | Declaración de variables con tipo incorrecto | `test_vars_bad_type.txt` | Error sintáctico |
| V04 | Declaración de variables sin punto y coma | `test_vars_missing_semi.txt` | Error sintáctico |
| V05 | Declaración de variables sin tipo | `test_vars_missing_type.txt` | Error sintáctico |

### 2.3. Pruebas de Funciones

| ID | Descripción | Archivo | Resultado Esperado |
|----|-------------|---------|-------------------|
| F01 | Función simple | `test_func_simple.txt` | Análisis exitoso, sin errores |
| F02 | Función con parámetros | `test_func_params.txt` | Análisis exitoso, sin errores |
| F03 | Función con variables locales | `test_func_local_vars.txt` | Análisis exitoso, sin errores |
| F04 | Función con cuerpo vacío | `test_func_empty.txt` | Error sintáctico |
| F05 | Función con parámetros mal formados | `test_func_bad_params.txt` | Error sintáctico |

### 2.4. Pruebas de Statements

| ID | Descripción | Archivo | Resultado Esperado |
|----|-------------|---------|-------------------|
| S01 | Asignación simple | `test_assign_simple.txt` | Análisis exitoso, sin errores |
| S02 | Condicional if-else | `test_condition.txt` | Análisis exitoso, sin errores |
| S03 | Ciclo while | `test_cycle.txt` | Análisis exitoso, sin errores |
| S04 | Llamada a función | `test_func_call.txt` | Análisis exitoso, sin errores |
| S05 | Statement print | `test_print.txt` | Análisis exitoso, sin errores |
| S06 | Statement print con múltiples expresiones | `test_print_multiple.txt` | Análisis exitoso, sin errores |

### 2.5. Pruebas de Expresiones

| ID | Descripción | Archivo | Resultado Esperado |
|----|-------------|---------|-------------------|
| E01 | Expresión aritmética simple | `test_expr_simple.txt` | Análisis exitoso, sin errores |
| E02 | Expresión con operadores de comparación | `test_expr_compare.txt` | Análisis exitoso, sin errores |
| E03 | Expresión con anidamiento de paréntesis | `test_expr_nested.txt` | Análisis exitoso, sin errores |
| E04 | Expresión con error de paréntesis | `test_expr_paren_error.txt` | Error sintáctico |
| E05 | Expresión con operadores en orden incorrecto | `test_expr_bad_order.txt` | Error sintáctico |

### 2.6. Pruebas de Programas Completos

| ID | Descripción | Archivo | Resultado Esperado |
|----|-------------|---------|-------------------|
| C01 | Programa completo válido | `test_complete_valid.txt` | Análisis exitoso, sin errores |
| C02 | Programa con combinación de statements | `test_mixed_statements.txt` | Análisis exitoso, sin errores |
| C03 | Programa con expresiones complejas | `test_complex_expr.txt` | Análisis exitoso, sin errores |
| C04 | Programa con combinación de errores | `test_mixed_errors.txt` | Error sintáctico |
| C05 | Programa con múltiples funciones y anidamiento | `test_advanced.txt` | Análisis exitoso, sin errores |

## 3. Archivos de Prueba

A continuación, se presentan los contenidos de algunos de los archivos de prueba más representativos:

### 3.1. test_min_valid.txt - Programa Mínimo Válido
```
program MinTest;
main {
    print("Hello World");
}
end
```

### 3.2. test_vars_multiple.txt - Declaración Múltiple de Variables
```
program VarsTest;
var
    x, y, z : int;
    a, b : float;
main {
    x = 10;
    print("x =", x);
}
end
```

### 3.3. test_func_params.txt - Función con Parámetros
```
program FuncTest;
void suma(a: int, b: int) {
    var
        result : int;
    result = a + b;
    print("Suma:", result);
};

main {
    suma(5, 10);
}
end
```

### 3.4. test_condition.txt - Condicional If-Else
```
program ConditionTest;
var
    x : int;
main {
    x = 10;
    if (x > 5) {
        print("x es mayor que 5");
    } else {
        print("x es menor o igual a 5");
    };
}
end
```

### 3.5. test_cycle.txt - Ciclo While
```
program CycleTest;
var
    i : int;
main {
    i = 0;
    while (i < 5) do {
        print("i =", i);
        i = i + 1;
    };
}
end
```

### 3.6. test_expr_nested.txt - Expresión con Anidamiento de Paréntesis
```
program ExprTest;
var
    result : int;
main {
    result = ((5 + 3) * 2) - (10 / (2 + 3));
    print("Resultado:", result);
}
end
```

### 3.7. test_complete_valid.txt - Programa Completo Válido
```
program CompleteTest;
var
    a, b, c : int;
    x, y : float;

void calculate(val: int, factor: float) {
    var
        result : float;
    result = val * factor;
    print("Resultado:", result);
};

main {
    a = 5;
    b = 10;
    c = a + b;
    
    x = 3.14;
    y = 2.71;
    
    if (c > 10) {
        print("c es mayor que 10");
        calculate(c, x);
    } else {
        print("c es menor o igual a 10");
    };
    
    while (a > 0) do {
        print("a =", a);
        a = a - 1;
    };
}
end
```

## 4. Procedimiento de Prueba

1. Generar el código del analizador sintáctico usando ANTLR:
   ```
   antlr4 -Dlanguage=Python3 LittleDuck.g4
   ```

2. Crear los archivos de prueba descritos en la sección 3.

3. Ejecutar el analizador sintáctico en cada archivo de prueba:
   ```
   python parser_runner.py <archivo_prueba> --tree
   ```

4. Verificar que los resultados coincidan con los esperados:
   - Los archivos válidos deben ser analizados sin errores y generar un árbol sintáctico correcto
   - Los archivos con errores deben generar mensajes de error adecuados

## 5. Criterios de Aceptación

El analizador sintáctico se considerará correcto si:

1. Reconoce correctamente todos los programas sintácticamente válidos (P01, V01, V02, F01, F02, F03, S01-S06, E01-E03, C01-C03, C05)
2. Reporta adecuadamente los errores en los programas inválidos (P02-P05, V03-V05, F04-F05, E04-E05, C04)
3. Genera árboles sintácticos que reflejan la estructura esperada según la gramática
4. No se presentan falsos positivos (programas incorrectos aceptados) ni falsos negativos (programas correctos rechazados)

## 6. Matriz de Cobertura

| Característica | Casos de Prueba |
|----------------|-----------------|
| Estructura básica del programa | P01-P05, C01-C05 |
| Declaración de variables | V01-V05, C01-C05 |
| Definición de funciones | F01-F05, C01, C05 |
| Asignaciones | S01, C01-C05 |
| Condicionales if-else | S02, C02, C05 |
| Ciclos while | S03, C02, C05 |
| Llamadas a funciones | S04, C01, C05 |
| Statements print | S05-S06, C01-C05 |
| Expresiones aritméticas | E01, E03-E05, C01-C05 |
| Expresiones de comparación | E02, C01-C05 |
| Anidamiento de expresiones | E03-E04, C03, C05 |
