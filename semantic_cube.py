# semantic_cube.py
from enum import Enum

# Define type constants using Enum
class Type(Enum):
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string' # For string literals, if needed for print
    BOOL = 'bool'   # Result of comparisons
    VOID = 'void'   # For function return types
    ERROR = 'error' # To represent a type mismatch

# Define operator constants using Enum
class Operator(Enum):
    PLUS = '+'
    MINUS = '-'
    MULT = '*'
    DIV = '/'
    LESS = '<'
    GREATER = '>'
    EQUAL = '=='
    NOT_EQUAL = '!='
    ASSIGN = '='
    UNARY_PLUS = 'unary+' # Added for semantic_analyzer.py
    UNARY_MINUS = 'unary-' # Added for semantic_analyzer.py
    # Add more operators as needed (AND, OR, etc.)

class SemanticCube:
    def __init__(self):
        self.cube = {}
        # Initialize the semantic cube rules
        # Format: self.cube[(type1, type2, operator)] = result_type

        # Arithmetic operations
        self._add_rule(Type.INT, Type.INT, Operator.PLUS, Type.INT)
        self._add_rule(Type.INT, Type.FLOAT, Operator.PLUS, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.INT, Operator.PLUS, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.PLUS, Type.FLOAT)

        self._add_rule(Type.INT, Type.INT, Operator.MINUS, Type.INT)
        self._add_rule(Type.INT, Type.FLOAT, Operator.MINUS, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.INT, Operator.MINUS, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.MINUS, Type.FLOAT)

        self._add_rule(Type.INT, Type.INT, Operator.MULT, Type.INT)
        self._add_rule(Type.INT, Type.FLOAT, Operator.MULT, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.INT, Operator.MULT, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.MULT, Type.FLOAT)

        self._add_rule(Type.INT, Type.INT, Operator.DIV, Type.FLOAT) # Division of ints can result in float
        self._add_rule(Type.INT, Type.FLOAT, Operator.DIV, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.INT, Operator.DIV, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.DIV, Type.FLOAT)

        # Relational operations
        self._add_rule(Type.INT, Type.INT, Operator.LESS, Type.BOOL)
        self._add_rule(Type.INT, Type.FLOAT, Operator.LESS, Type.BOOL)
        self._add_rule(Type.FLOAT, Type.INT, Operator.LESS, Type.BOOL)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.LESS, Type.BOOL)

        self._add_rule(Type.INT, Type.INT, Operator.GREATER, Type.BOOL)
        self._add_rule(Type.INT, Type.FLOAT, Operator.GREATER, Type.BOOL)
        self._add_rule(Type.FLOAT, Type.INT, Operator.GREATER, Type.BOOL)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.GREATER, Type.BOOL)

        self._add_rule(Type.INT, Type.INT, Operator.EQUAL, Type.BOOL)
        self._add_rule(Type.INT, Type.FLOAT, Operator.EQUAL, Type.BOOL) # Allow comparison between int and float
        self._add_rule(Type.FLOAT, Type.INT, Operator.EQUAL, Type.BOOL)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.EQUAL, Type.BOOL)
        self._add_rule(Type.BOOL, Type.BOOL, Operator.EQUAL, Type.BOOL) # Allow bool == bool

        self._add_rule(Type.INT, Type.INT, Operator.NOT_EQUAL, Type.BOOL)
        self._add_rule(Type.INT, Type.FLOAT, Operator.NOT_EQUAL, Type.BOOL)
        self._add_rule(Type.FLOAT, Type.INT, Operator.NOT_EQUAL, Type.BOOL)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.NOT_EQUAL, Type.BOOL)
        self._add_rule(Type.BOOL, Type.BOOL, Operator.NOT_EQUAL, Type.BOOL) # Allow bool != bool

        # Assignment operations
        self._add_rule(Type.INT, Type.INT, Operator.ASSIGN, Type.INT) # Target type, value type, op, result (usually target type or error)
        self._add_rule(Type.FLOAT, Type.FLOAT, Operator.ASSIGN, Type.FLOAT)
        self._add_rule(Type.FLOAT, Type.INT, Operator.ASSIGN, Type.FLOAT) # Assigning int to float is ok
        self._add_rule(Type.BOOL, Type.BOOL, Operator.ASSIGN, Type.BOOL) # Allow bool = bool
        # Assigning float to int (Type.INT, Type.FLOAT, Operator.ASSIGN) is intentionally omitted,
        # so it will default to Type.ERROR in get_type.

        # Rules for unary operators (optional, can be handled directly in analyzer)
        # Example: self._add_rule(Type.INT, None, Operator.UNARY_MINUS, Type.INT)
        # For unary, type2 might be None or a special marker.
        # The get_type method would need to handle calls with two or three arguments.
        # Alternatively, have a get_unary_type(type1, operator)

        # Unary operations (using Type.VOID as the second operand type for convention)
        self._add_rule(Type.INT, Type.VOID, Operator.UNARY_PLUS, Type.INT)
        self._add_rule(Type.FLOAT, Type.VOID, Operator.UNARY_PLUS, Type.FLOAT)
        self._add_rule(Type.INT, Type.VOID, Operator.UNARY_MINUS, Type.INT)
        self._add_rule(Type.FLOAT, Type.VOID, Operator.UNARY_MINUS, Type.FLOAT)

    def _add_rule(self, type1: Type, type2: Type, operator: Operator, result_type: Type):
        self.cube[(type1, type2, operator)] = result_type

    def get_type(self, type1: Type, type2: Type, operator: Operator) -> Type:
        """
        Gets the result type for a binary operation.
        For unary operations, type2 should be Type.VOID.
        """
        return self.cube.get((type1, type2, operator), Type.ERROR)

# Example usage:
if __name__ == '__main__':
    cube = SemanticCube()
    print(f"int + int = {cube.get_type(Type.INT, Type.INT, Operator.PLUS).value}")
    print(f"int + float = {cube.get_type(Type.INT, Type.FLOAT, Operator.PLUS).value}")
    print(f"int / int = {cube.get_type(Type.INT, Type.INT, Operator.DIV).value}")
    print(f"int == float = {cube.get_type(Type.INT, Type.FLOAT, Operator.EQUAL).value}")
    print(f"bool == bool = {cube.get_type(Type.BOOL, Type.BOOL, Operator.EQUAL).value}")
    
    # Test assignment
    print(f"Assign int to float var (float = int): {cube.get_type(Type.FLOAT, Type.INT, Operator.ASSIGN).value}")
    print(f"Assign float to int var (int = float): {cube.get_type(Type.INT, Type.FLOAT, Operator.ASSIGN).value}") # Expected: error
    print(f"Assign bool to bool var (bool = bool): {cube.get_type(Type.BOOL, Type.BOOL, Operator.ASSIGN).value}")

    # Test unary operations
    print(f"Unary minus for int: {cube.get_type(Type.INT, Type.VOID, Operator.UNARY_MINUS).value}")
    print(f"Unary plus for float: {cube.get_type(Type.FLOAT, Type.VOID, Operator.UNARY_PLUS).value}")
    print(f"Unary minus for bool (error): {cube.get_type(Type.BOOL, Type.VOID, Operator.UNARY_MINUS).value}")
    
    # Test a missing rule (should return ERROR)
    print(f"string + int = {cube.get_type(Type.STRING, Type.INT, Operator.PLUS).value}")
