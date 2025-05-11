# Test Plan para el Analizador Léxico de LittleDuck

## 1. Objetivos de las Pruebas

El objetivo principal de este test plan es verificar que el analizador léxico desarrollado pueda:

1. Identificar correctamente todos los tokens definidos en la gramática
2. Manejar adecuadamente casos de entrada válidos e inválidos
3. Ignorar correctamente espacios en blanco y comentarios
4. Reportar errores léxicos cuando sea apropiado

## 2. Casos de Prueba

### 2.1. Pruebas de Tokens Individuales

| ID | Descripción | Entrada | Resultado Esperado |
|----|-------------|---------|-------------------|
| T01 | Palabras reservadas | `program main end var int float print while do if else void` | Cada palabra debe ser reconocida como su token correspondiente |
| T02 | Delimitadores | `; , : { } ( ) [ ]` | Cada delimitador debe ser reconocido como su token correspondiente |
| T03 | Operadores | `= == != > < + - * /` | Cada operador debe ser reconocido como su token correspondiente |
| T04 | Identificadores válidos | `variable x123 nombre_variable someVar` | Cada identificador debe ser reconocido como token ID |
| T05 | Identificadores inválidos | `123var _var` | El primero debe generar tokens numéricos y el segundo un error léxico |
| T06 | Enteros | `0 123 9999` | Cada número debe ser reconocido como token CTE_INT |
| T07 | Flotantes | `0.5 123.456 9999.0` | Cada número debe ser reconocido como token CTE_FLOAT |
| T08 | Strings | `"Hola mundo" "123" ""` | Cada string debe ser reconocido como token CTE_STR |

### 2.2. Pruebas de Programas Completos

| ID | Descripción | Archivo | Resultado Esperado |
|----|-------------|---------|-------------------|
| P01 | Programa mínimo | `test_min.txt` | Todos los tokens deben ser reconocidos correctamente |
| P02 | Programa con variables | `test_var.txt` | Todos los tokens deben ser reconocidos correctamente |
| P03 | Programa con estructuras de control | `test_control.txt` | Todos los tokens deben ser reconocidos correctamente |
| P04 | Programa completo | `test_complete.txt` | Todos los tokens deben ser reconocidos correctamente |
| P05 | Programa con errores léxicos | `test_errors.txt` | Los errores léxicos deben ser reportados correctamente |

## 3. Archivos de Prueba

A continuación, se presentan los contenidos de los archivos de prueba que se utilizarán:

### 3.1. test_min.txt - Programa Mínimo
```
program MinTest {
    main() {
        print("Hello World");
    }
}
end
```

### 3.2. test_var.txt - Programa con Variables
```
program VarTest {
    var 
        x, y : int;
        z : float;
    
    main() {
        x = 10;
        y = 20;
        z = 3.14;
        print("x + y =", x + y);
    }
}
end
```

### 3.3. test_control.txt - Programa con Estructuras de Control
```
program ControlTest {
    var
        i : int;
        max : int;
    
    main() {
        max = 5;
        i = 0;
        
        while (i < max) do {
            if (i == 3) {
                print("Encontrado: 3");
            } else {
                print("Valor:", i);
            }
            i = i + 1;
        }
    }
}
end
```

### 3.4. test_complete.txt - Programa Completo
```
program CompleteTest {
    var
        a, b, c : int;
        x, y : float;
        name : int;
    
    main() {
        a = 5;
        b = 10;
        c = a + b * 2;
        
        x = 3.14;
        y = 2.71;
        
        if (c > 20) {
            print("c es mayor que 20");
        } else {
            print("c es menor o igual a 20");
        }
        
        name = 0;
        while (name < 5) do {
            print("Iteración:", name);
            name = name + 1;
        }
    }
}
end
```

### 3.5. test_errors.txt - Programa con Errores Léxicos
```
program ErrorTest {
    var
        123var : int;  // Identificador inválido
        x% : float;    // Carácter inválido
    
    main() {
        print("String no cerrado);  // String sin cerrar
        y = 10..5;     // Número flotante inválido
    }
}
end
```

## 4. Procedimiento de Prueba

1. Generar el código del analizador léxico usando ANTLR:
   ```
   antlr4 -Dlanguage=Python3 LittleDuck.g4
   ```

2. Crear los archivos de prueba descritos en la sección 3.

3. Ejecutar el analizador léxico en cada archivo de prueba:
   ```
   python lexer_runner.py tests/lexer/test_min.txt
   python lexer_runner.py tests/lexer/test_var.txt
   python lexer_runner.py tests/lexer/test_control.txt
   python lexer_runner.py tests/lexer/test_complete.txt
   python lexer_runner.py tests/lexer/test_errors.txt
   ```

4. Verificar que los resultados coincidan con los esperados.

## 5. Criterios de Aceptación

El analizador léxico se considerará correcto si:

1. Identifica correctamente todos los tokens en los archivos de prueba válidos (P01-P04)
2. Reporta adecuadamente los errores en el archivo de prueba con errores (P05)
3. La cantidad de tokens identificados coincide con la esperada en cada caso
4. No se presentan falsos positivos ni falsos negativos

## 6. Matriz de Cobertura

| Característica | Casos de Prueba |
|----------------|-----------------|
| Palabras reservadas | T01, P01-P05 |
| Delimitadores | T02, P01-P05 |
| Operadores | T03, P02-P05 |
| Identificadores | T04, T05, P01-P05 |
| Constantes enteras | T06, P02-P05 |
| Constantes flotantes | T07, P02-P05 |
| Constantes string | T08, P01-P05 |
| Manejo de errores | T05, P05 |
