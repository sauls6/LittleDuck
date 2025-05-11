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
LBRACK     : '[';
RBRACK     : ']';

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


// Parser rules

program
    : PROGRAM ID SEMI vars? funcs? MAIN body END
    ;

vars
    : VAR (ID (COMMA ID)* COLON type SEMI)+
    ;

funcs
    : (VOID ID LPAREN param_list? RPAREN LBRACK vars? body RBRACK SEMI)+
    ;

param_list
    : (ID COLON type) (COMMA ID COLON type)*
    ;

type
    : INTTYPE
    | FLTTYPE
    ;

body
    : LBRACE statement* RBRACE
    ;



statement
    : assignment
    | condition
    | cycle
    | f_call
    | print_stmt
    ;

assignment
    : ID ASSIGN expression SEMI
    ;

condition
    : IF LPAREN expression RPAREN body (ELSE body)? SEMI
    ;

// pensando que el diagrama esta mal el orden de body y expression, o que
// puede que querian un do-while, pero no lo especifica bien tmp
cycle
    : WHILE LPAREN expression RPAREN DO body SEMI
    ;
//expression, en print y functioncall
f_call
    : ID LPAREN expression_multiple? RPAREN SEMI
    ;

print_args
    : (CTE_STR | expression) (COMMA (CTE_STR | expression))*
    ;

print_stmt
    : PRINT LPAREN print_args RPAREN SEMI
    ;

expression_multiple
    : expression (COMMA expression)*
    ;

expression
    : exp ((LESS | GREATER | EQUAL | NOT_EQUAL) exp)?
    ;

exp
    : term ((PLUS | MINUS) term)*
    ;

term
    : factor ((MULT | DIV) factor)*
    ;

/* num_construct
    : (PLUS | MINUS)? (CTE_INT | CTE_FLOAT)
    ; */

factor // expressions in parentheses cant have unary operators, but numbers and ids can
    : LPAREN expression RPAREN
    | (PLUS | MINUS)? ID
    | (PLUS | MINUS)? (CTE_INT | CTE_FLOAT)
    ;

/* 
factor // more advanced version that allows unary operators and functions inside factor
    : (PLUS | MINUS)? (LPAREN expression RPAREN
                      | ID (LPAREN expression_multiple RPAREN)?
                      | num_construct)
    ; */
