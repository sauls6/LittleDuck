grammar LittleDuck;

// Palabras reservadas
PROGRAM    : 'program';
MAIN       : 'main';
END        : 'end';
VAR        : 'var';
INTTYPE    : 'int';
FLTTYPE    : 'float';
PRINT      : 'print';
WHILE      : 'while';
DO         : 'do';
IF         : 'if';
ELSE       : 'else';
VOID       : 'void';

// Delimitadores
SEMI       : ';';
COMMA      : ',';
COLON      : ':';
LBRACE     : '{';
RBRACE     : '}';
LPAREN     : '(';
RPAREN     : ')';
LSQUAR     : '[';
RSQUAR     : ']';

// Operadores
ASSIGN     : '=';
EQUAL      : '==';
NOT_EQUAL  : '!=';
GREATER    : '>';
LESS       : '<';
PLUS       : '+';
MINUS      : '-';
MULT       : '*';
DIV        : '/';

// Identificadores y Constantes
ID         : [a-zA-Z] [a-zA-Z0-9_]* ;
CTE_INT    : [0-9]+ ;
CTE_FLOAT  : [0-9]+ '.' [0-9]+ ;
CTE_STR    : '"' (~["\n\r])* '"' ;

// Ignorar espacios en blanco y saltos de línea
WS         : [ \t\r\n]+ -> skip ;
