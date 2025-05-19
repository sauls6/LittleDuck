# filepath: c:\Users\sauls\PycharmProjects\LittleDuck\semantic_analyzer.py
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from gen.LittleDuckLexer import LittleDuckLexer
from gen.LittleDuckParser import LittleDuckParser
from gen.LittleDuckVisitor import LittleDuckVisitor
from symbol_table import SymbolTable, FunctionEntry, VariableEntry
from semantic_cube import SemanticCube, Type, Operator

class SemanticAnalyzer(LittleDuckVisitor):
    def __init__(self, symbol_table: SymbolTable, semantic_cube: SemanticCube):
        super().__init__()
        self.symbol_table = symbol_table
        self.semantic_cube = semantic_cube
        self.errors = []
        self.current_scope_name = 'global'
        self.operand_stack = [] 
        self.operator_stack = [] 

    def add_error(self, message, ctx):
        line = -1
        column = -1
        if hasattr(ctx, 'start') and ctx.start is not None:
            line = ctx.start.line
            column = ctx.start.column
        elif hasattr(ctx, 'line'): 
            line = ctx.line
            column = ctx.column
        self.errors.append(f"Error at Line {line}:{column} - {message}")

    def visitProgram(self, ctx:LittleDuckParser.ProgramContext):
        self.current_scope_name = 'global'
        self.symbol_table.set_current_scope('global')

        prog_id_token = ctx.ID().getSymbol()
        # Optional: Add program name to a special part of symbol table or just note it.
        # self.symbol_table.add_program_id(prog_id_token.text)


        if ctx.vars_(): 
            self.visit(ctx.vars_())

        if ctx.funcs(): 
            self.visit(ctx.funcs())

        user_defined_main = self.symbol_table.get_function('main')
        main_func_entry = None

        if user_defined_main:
            if user_defined_main.param_count > 0:
                main_token = ctx.MAIN().symbol if ctx.MAIN() else prog_id_token
                self.add_error(f"User-defined function 'main' must not have parameters.", main_token)
            main_func_entry = user_defined_main
        else:
            main_func_entry = self.symbol_table.add_function('main', Type.VOID)
            if not main_func_entry:
                self.add_error(f"Critical error: Failed to create implicit 'main' function scope.", ctx.MAIN().symbol if ctx.MAIN() else prog_id_token)
                return self.errors
        
        if not main_func_entry: # Should be redundant if logic above is correct
            self.add_error(f"Critical error: Could not establish 'main' function entry.", ctx.MAIN().symbol if ctx.MAIN() else prog_id_token)
            return self.errors

        self.current_scope_name = 'main'
        self.symbol_table.set_current_scope('main')
        
        if not ctx.MAIN():
            self.add_error("Missing MAIN keyword for program entry point.", prog_id_token) # Error near program ID or start

        if ctx.body():
            self.visit(ctx.body())
        else:
            main_token_for_error = ctx.MAIN().symbol if ctx.MAIN() else prog_id_token
            self.add_error("Program 'main' block is missing a body.", main_token_for_error)


        self.current_scope_name = 'global' 
        self.symbol_table.set_current_scope('global')
        return self.errors

    def visitVars(self, ctx:LittleDuckParser.VarsContext):
        if not ctx.children or len(ctx.children) <= 1: # Needs at least VAR and one declaration
            if ctx.getText() and ctx.getText().strip() != "var": # if only "var" is present, it's an empty block
                 self.add_error("Empty or malformed var block.", ctx)
            return self.errors

        children = ctx.children
        num_children = len(children)
        idx = 0

        if idx < num_children and isinstance(children[idx], TerminalNodeImpl) and \
           children[idx].symbol.type == LittleDuckLexer.VAR:
            idx += 1

        while idx < num_children:
            current_ids_nodes = []
            start_of_decl_item = children[idx] if idx < num_children else ctx # For error reporting

            while idx < num_children:
                child = children[idx]
                if isinstance(child, TerminalNodeImpl):
                    if child.symbol.type == LittleDuckLexer.ID:
                        current_ids_nodes.append(child)
                        idx += 1
                    elif child.symbol.type == LittleDuckLexer.COMMA:
                        idx += 1 
                    else: 
                        break
                else: 
                    break 
            
            if not current_ids_nodes:
                if idx < num_children : # If there are still children but no IDs were parsed
                     self.add_error("Expected variable name(s) in declaration.", children[idx])
                break 

            if idx < num_children and isinstance(children[idx], TerminalNodeImpl) and \
               children[idx].symbol.type == LittleDuckLexer.COLON:
                idx += 1
            else:
                err_ctx = current_ids_nodes[-1] if current_ids_nodes else (children[idx-1] if idx > 0 else start_of_decl_item)
                self.add_error("Expected ':' after variable names.", err_ctx)
                break 

            var_type_val = None
            type_ctx_for_err = None
            if idx < num_children and isinstance(children[idx], LittleDuckParser.TypeContext):
                type_ctx_for_err = children[idx]
                var_type_val = self.visit(type_ctx_for_err)
                idx += 1
            else:
                err_ctx = children[idx-1] if idx > 0 else start_of_decl_item
                self.add_error("Expected type (int/float) after ':'.", err_ctx)
                break

            if idx < num_children and isinstance(children[idx], TerminalNodeImpl) and \
               children[idx].symbol.type == LittleDuckLexer.SEMI:
                idx += 1
            else:
                err_ctx = type_ctx_for_err if type_ctx_for_err else (children[idx-1] if idx > 0 else start_of_decl_item)
                self.add_error("Expected ';' after type declaration.", err_ctx)
                break 

            if var_type_val and var_type_val != Type.ERROR:
                for id_node in current_ids_nodes:
                    var_name = id_node.getText()
                    added_successfully = False
                    if self.current_scope_name == 'global':
                        added_successfully = self.symbol_table.add_global_variable(var_name, var_type_val)
                        if not added_successfully:
                            self.add_error(f"Global variable '{var_name}' already declared.", id_node)
                    else:
                        current_func = self.symbol_table.get_function(self.current_scope_name)
                        if current_func:
                            added_successfully = current_func.add_variable(var_name, var_type_val)
                            if not added_successfully:
                                self.add_error(f"Variable '{var_name}' already declared in function '{self.current_scope_name}'.", id_node)
                        else:
                            self.add_error(f"Internal error: Cannot find function scope '{self.current_scope_name}' for var '{var_name}'.", id_node)
            elif not var_type_val or var_type_val == Type.ERROR:
                 err_node_for_type = type_ctx_for_err if type_ctx_for_err else (children[idx-1] if idx > 0 and isinstance(children[idx-1], LittleDuckParser.TypeContext) else start_of_decl_item)
                 self.add_error(f"Invalid type for variables {', '.join([id_n.getText() for id_n in current_ids_nodes])}.", err_node_for_type)
        return self.errors

    def visitFuncs(self, ctx:LittleDuckParser.FuncsContext):
        # Grammar: (VOID ID LPAREN param_list? RPAREN LBRACK vars? body RBRACK SEMI)+
        # Iterate through the children of FuncsContext. Each function definition is a sequence.
        children = ctx.children
        if not children:
            return self.errors
            
        idx = 0
        num_children = len(children)

        while idx < num_children:
            # Mark the start of a potential function definition
            start_idx_for_func = idx

            # Expect VOID
            if not (idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.VOID):
                if children[idx].getText() != "<EOF>": # Avoid error on EOF
                    self.add_error("Expected 'void' to start function definition.", children[idx])
                idx +=1 # Try to recover by skipping to next token
                continue 
            void_token_node = children[idx]
            idx += 1

            # Expect ID (function name)
            if not (idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.ID):
                self.add_error("Expected function name after 'void'.", void_token_node)
                # Attempt to find next SEMI or VOID to recover for next function
                while idx < num_children and not (isinstance(children[idx], TerminalNodeImpl) and (children[idx].symbol.type == LittleDuckLexer.SEMI or children[idx].symbol.type == LittleDuckLexer.VOID)):
                    idx += 1
                if idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI: idx +=1 # consume SEMI
                continue
            func_name_node = children[idx]
            func_name = func_name_node.getText()
            idx += 1

            if self.symbol_table.get_function(func_name):
                self.add_error(f"Function '{func_name}' redeclared.", func_name_node)
                # Skip to end of this malformed function definition (e.g., find SEMI)
                while idx < num_children and not (isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI):
                    idx += 1
                if idx < num_children: idx +=1 # consume SEMI
                continue

            func_entry = self.symbol_table.add_function(func_name, Type.VOID)
            if not func_entry: # Should be caught by get_function above
                self.add_error(f"Internal error: Failed to add function '{func_name}' to symbol table.", func_name_node)
                # Skip to end of this malformed function
                while idx < num_children and not (isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI):
                    idx += 1
                if idx < num_children: idx +=1
                continue
            
            previous_scope = self.current_scope_name
            self.current_scope_name = func_name
            self.symbol_table.set_current_scope(func_name)

            # Expect LPAREN
            if not (idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.LPAREN):
                self.add_error(f"Expected '(' after function name '{func_name}'.", func_name_node)
                self.current_scope_name = previous_scope; self.symbol_table.set_current_scope(previous_scope) # Revert scope
                while idx < num_children and not (isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI): idx += 1
                if idx < num_children: idx +=1
                continue
            idx += 1

            # Optional Param_list
            if idx < num_children and isinstance(children[idx], LittleDuckParser.Param_listContext):
                self.visit(children[idx]) # visitParam_list
                idx += 1
            
            # Expect RPAREN
            if not (idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.RPAREN):
                self.add_error(f"Expected ')' after parameters for function '{func_name}'.", children[idx-1] if idx > 0 else func_name_node)
                self.current_scope_name = previous_scope; self.symbol_table.set_current_scope(previous_scope)
                while idx < num_children and not (isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI): idx += 1
                if idx < num_children: idx +=1
                continue
            idx += 1

            # Expect LBRACK
            if not (idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.LBRACK):
                self.add_error(f"Expected '[' before function body for '{func_name}'.", children[idx-1] if idx > 0 else func_name_node)
                self.current_scope_name = previous_scope; self.symbol_table.set_current_scope(previous_scope)
                while idx < num_children and not (isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI): idx += 1
                if idx < num_children: idx +=1
                continue
            idx += 1
            
            # Optional Vars
            if idx < num_children and isinstance(children[idx], LittleDuckParser.VarsContext):
                self.visit(children[idx]) # Local variables for the function
                idx += 1

            # Expect Body
            if idx < num_children and isinstance(children[idx], LittleDuckParser.BodyContext):
                self.visit(children[idx])
                idx += 1
            else:
                self.add_error(f"Function '{func_name}' is missing a body.", children[idx-1] if idx > 0 else func_name_node)
                # No body, but still need to look for RBRACK and SEMI to recover

            # Expect RBRACK
            if not (idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.RBRACK):
                self.add_error(f"Expected ']' after function body for '{func_name}'.", children[idx-1] if idx > 0 else func_name_node)
                # Error recovery: try to find SEMI
                self.current_scope_name = previous_scope; self.symbol_table.set_current_scope(previous_scope)
                while idx < num_children and not (isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI): idx += 1
                if idx < num_children: idx +=1
                continue
            idx += 1

            # Expect SEMI
            if not (idx < num_children and isinstance(children[idx], TerminalNodeImpl) and children[idx].symbol.type == LittleDuckLexer.SEMI):
                self.add_error(f"Expected ';' after function definition for '{func_name}'.", children[idx-1] if idx > 0 else func_name_node)
                # SEMI might be missing, but we are at the logical end of this function.
                # If next token is VOID, it will be caught at the start of the outer loop.
            else:
                idx += 1 # Consume SEMI

            self.current_scope_name = previous_scope
            self.symbol_table.set_current_scope(previous_scope)
        
        return self.errors


    def visitParam_list(self, ctx:LittleDuckParser.Param_listContext):
        func_entry = self.symbol_table.get_function(self.current_scope_name)
        if not func_entry:
            self.add_error(f"Internal error: Cannot add parameters, function scope '{self.current_scope_name}' not found.", ctx)
            return

        id_nodes = ctx.ID()
        type_nodes = ctx.type_() 

        if len(id_nodes) != len(type_nodes):
            self.add_error(f"Parameter list malformed: mismatch count of IDs and types in function '{self.current_scope_name}'.", ctx)
            return

        for i in range(len(id_nodes)):
            param_name_token_node = id_nodes[i]
            param_name = param_name_token_node.getSymbol().text
            type_ctx = type_nodes[i] 
            param_type = self.visit(type_ctx)

            if param_type == Type.ERROR:
                self.add_error(f"Invalid type for parameter '{param_name}' in function '{self.current_scope_name}'.", type_ctx)
                continue 

            if not func_entry.add_param(param_name, param_type): 
                self.add_error(f"Parameter '{param_name}' redeclared in function '{self.current_scope_name}'.", param_name_token_node.getSymbol())
        return None

    def visitType(self, ctx:LittleDuckParser.TypeContext):
        type_text = ctx.getText()
        if type_text == 'int':
            return Type.INT
        elif type_text == 'float':
            return Type.FLOAT
        else:
            self.add_error(f"Unknown type '{type_text}'.", ctx)
            return Type.ERROR

    def visitBody(self, ctx:LittleDuckParser.BodyContext):
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if isinstance(child, LittleDuckParser.StatementContext):
                self.visit(child)
        return None

    def visitStatement(self, ctx:LittleDuckParser.StatementContext):
        return self.visitChildren(ctx)


    def visitAssignment(self, ctx:LittleDuckParser.AssignmentContext):
        var_name_token = ctx.ID().getSymbol()
        var_name = var_name_token.text

        var_entry = self.symbol_table.get_variable_in_scope(var_name, self.current_scope_name)
        if not var_entry:
            self.add_error(f"Variable '{var_name}' not declared before assignment.", var_name_token)
            self.visit(ctx.expression()) 
            if self.operand_stack: self.operand_stack.pop() 
            return None
        
        target_type = var_entry.type

        self.visit(ctx.expression())
        if not self.operand_stack:
            self.add_error(f"Could not determine type of expression in assignment to '{var_name}'.", ctx.expression())
            return None
        
        expr_type = self.operand_stack.pop()

        if expr_type == Type.ERROR: 
            return None

        assign_result_type = self.semantic_cube.get_type(target_type, expr_type, Operator.ASSIGN)

        if assign_result_type == Type.ERROR:
            self.add_error(f"Type mismatch: cannot assign type '{expr_type.value}' to variable '{var_name}' of type '{target_type.value}'.", var_name_token)
        return None

    def visitExpression(self, ctx:LittleDuckParser.ExpressionContext):
        self.visit(ctx.exp(0)) 

        if len(ctx.exp()) > 1: 
            if not self.operand_stack: 
                 self.add_error("Left operand missing for relational operator.", ctx.exp(0))
                 self.operand_stack.append(Type.ERROR) 
                 self.visit(ctx.exp(1))
                 if self.operand_stack: self.operand_stack.pop() 
                 return

            left_type = self.operand_stack.pop()
            
            op_token = ctx.getChild(1).getSymbol() 
            op_text = op_token.text
            actual_operator = None
            if op_text == '<': actual_operator = Operator.LESS
            elif op_text == '>': actual_operator = Operator.GREATER
            elif op_text == '==': actual_operator = Operator.EQUAL
            elif op_text == '!=': actual_operator = Operator.NOT_EQUAL
            else:
                self.add_error(f"Unknown relational operator '{op_text}'.", op_token)
                self.operand_stack.append(Type.ERROR) 
                self.visit(ctx.exp(1)) 
                if self.operand_stack: self.operand_stack.pop()
                return

            self.visit(ctx.exp(1)) 
            if not self.operand_stack: 
                self.add_error("Right operand missing for relational operator.", ctx.exp(1))
                self.operand_stack.append(Type.ERROR) 
                return

            right_type = self.operand_stack.pop()

            if left_type == Type.ERROR or right_type == Type.ERROR:
                self.operand_stack.append(Type.ERROR) 
                return

            result_type = self.semantic_cube.get_type(left_type, right_type, actual_operator)
            if result_type == Type.ERROR:
                self.add_error(f"Type mismatch: cannot compare '{left_type.value}' with '{right_type.value}' using operator '{op_text}'.", op_token)
            self.operand_stack.append(result_type) 
        return None

    def visitExp(self, ctx:LittleDuckParser.ExpContext):
        self.visit(ctx.term(0)) 

        for i in range(len(ctx.term()) - 1): 
            if not self.operand_stack:
                self.add_error(f"Left operand missing for operator.", ctx.term(i))
                self.operand_stack.append(Type.ERROR) 
                self.visit(ctx.term(i + 1)) 
                if self.operand_stack: self.operand_stack.pop() 
                return 

            left_type = self.operand_stack.pop()
            
            op_node = ctx.getChild(i * 2 + 1) 
            op_token = op_node.getSymbol()
            op_text = op_token.text
            actual_operator = None
            if op_text == '+': actual_operator = Operator.PLUS
            elif op_text == '-': actual_operator = Operator.MINUS
            else: 
                self.add_error(f"Unknown operator '{op_text}' in exp.", op_token)
                self.operand_stack.append(Type.ERROR)
                self.visit(ctx.term(i + 1)) 
                if self.operand_stack: self.operand_stack.pop() 
                return

            self.visit(ctx.term(i + 1)) 
            if not self.operand_stack:
                self.add_error(f"Right operand missing for '{op_text}'.", ctx.term(i+1))
                self.operand_stack.append(Type.ERROR)
                return

            right_type = self.operand_stack.pop()

            if left_type == Type.ERROR or right_type == Type.ERROR:
                self.operand_stack.append(Type.ERROR)
                return

            result_type = self.semantic_cube.get_type(left_type, right_type, actual_operator)
            if result_type == Type.ERROR:
                self.add_error(f"Type mismatch for operator '{op_text}' with operands '{left_type.value}' and '{right_type.value}'.", op_token)
            self.operand_stack.append(result_type)
        return None

    def visitTerm(self, ctx:LittleDuckParser.TermContext):
        self.visit(ctx.factor(0)) 

        for i in range(len(ctx.factor()) - 1):
            if not self.operand_stack:
                self.add_error(f"Left operand missing for operator.", ctx.factor(i))
                self.operand_stack.append(Type.ERROR)
                self.visit(ctx.factor(i + 1))
                if self.operand_stack: self.operand_stack.pop()
                return

            left_type = self.operand_stack.pop()

            op_node = ctx.getChild(i * 2 + 1) 
            op_token = op_node.getSymbol()
            op_text = op_token.text
            actual_operator = None
            if op_text == '*': actual_operator = Operator.MULT
            elif op_text == '/': actual_operator = Operator.DIV
            else: 
                self.add_error(f"Unknown operator '{op_text}' in term.", op_token)
                self.operand_stack.append(Type.ERROR)
                self.visit(ctx.factor(i + 1))
                if self.operand_stack: self.operand_stack.pop()
                return

            self.visit(ctx.factor(i + 1)) 
            if not self.operand_stack:
                self.add_error(f"Right operand missing for '{op_text}'.", ctx.factor(i+1))
                self.operand_stack.append(Type.ERROR)
                return
            
            right_type = self.operand_stack.pop()

            if left_type == Type.ERROR or right_type == Type.ERROR:
                self.operand_stack.append(Type.ERROR)
                return
                
            result_type = self.semantic_cube.get_type(left_type, right_type, actual_operator)
            if result_type == Type.ERROR:
                self.add_error(f"Type mismatch for operator '{op_text}' with operands '{left_type.value}' and '{right_type.value}'.", op_token)
            self.operand_stack.append(result_type)
        return None

    def visitFactor(self, ctx:LittleDuckParser.FactorContext):
        # Grammar: (PLUS | MINUS)? (LPAREN expression RPAREN | ID | (CTE_INT | CTE_FLOAT))
        
        has_unary_op = False
        unary_op_token = None
        actual_factor_node_index = 0 # Index of the actual factor part (ID, CTE, or LPAREN)

        # Check for leading PLUS or MINUS
        if isinstance(ctx.getChild(0), TerminalNodeImpl):
            first_child_symbol = ctx.getChild(0).getSymbol()
            if first_child_symbol.type == LittleDuckLexer.PLUS or first_child_symbol.type == LittleDuckLexer.MINUS:
                has_unary_op = True
                unary_op_token = first_child_symbol
                actual_factor_node_index = 1 # The factor itself is the second child
        
        factor_content_node = ctx.getChild(actual_factor_node_index)

        base_type = Type.ERROR

        if isinstance(factor_content_node, LittleDuckParser.ExpressionContext): # LPAREN expression RPAREN
            if has_unary_op: # Grammar is (PLUS|MINUS)? ( (LPAREN expr RPAREN) | ID | CONST )
                             # So, unary can apply to (expression)
                self.visit(factor_content_node) # visit expression
                if self.operand_stack:
                    base_type = self.operand_stack.pop()
                else: # Error in sub-expression
                    self.add_error("Could not determine type of parenthesized expression for unary op.", factor_content_node)
                    self.operand_stack.append(Type.ERROR)
                    return
            else: # Just (expression)
                self.visit(factor_content_node) # type will be left on stack
                return # Do not apply unary logic again

        elif isinstance(factor_content_node, TerminalNodeImpl) and factor_content_node.getSymbol().type == LittleDuckLexer.ID:
            var_name = factor_content_node.getSymbol().text
            var_entry = self.symbol_table.get_variable_in_scope(var_name, self.current_scope_name)
            if not var_entry:
                self.add_error(f"Variable '{var_name}' not declared.", factor_content_node.getSymbol())
                base_type = Type.ERROR
            else:
                base_type = var_entry.type
        
        elif isinstance(factor_content_node, TerminalNodeImpl) and factor_content_node.getSymbol().type == LittleDuckLexer.CTE_INT:
            base_type = Type.INT

        elif isinstance(factor_content_node, TerminalNodeImpl) and factor_content_node.getSymbol().type == LittleDuckLexer.CTE_FLOAT:
            base_type = Type.FLOAT
            
        else: # Should not be reached
            self.add_error("Invalid factor structure.", ctx)
            self.operand_stack.append(Type.ERROR)
            return

        if base_type == Type.ERROR: # If base_type couldn't be determined (e.g. undeclared ID)
            self.operand_stack.append(Type.ERROR)
            return

        if has_unary_op:
            op_enum = Operator.UNARY_PLUS if unary_op_token.type == LittleDuckLexer.PLUS else Operator.UNARY_MINUS
            # Use Type.VOID as the second operand for unary ops in semantic cube
            result_type = self.semantic_cube.get_type(base_type, Type.VOID, op_enum) 
            if result_type == Type.ERROR:
                self.add_error(f"Unary operator '{unary_op_token.text}' cannot be applied to type '{base_type.value}'.", unary_op_token)
                self.operand_stack.append(Type.ERROR)
            else:
                self.operand_stack.append(result_type)
        else:
            self.operand_stack.append(base_type)
        return None

    def visitPrint_stmt(self, ctx:LittleDuckParser.Print_stmtContext):
        print_args_ctx = ctx.print_args()
        if not print_args_ctx: 
            self.add_error("Empty print statement arguments.", ctx.LPAREN().getSymbol())
            return None

        # Iterate through children of print_args_ctx to handle expressions and CTE_STR in order
        for child_arg in print_args_ctx.children:
            if isinstance(child_arg, LittleDuckParser.ExpressionContext):
                self.visit(child_arg)
                if not self.operand_stack:
                    self.add_error("Could not determine type of expression in print statement.", child_arg)
                else:
                    expr_type = self.operand_stack.pop()
                    if expr_type == Type.VOID: 
                        self.add_error("Cannot print expression of type VOID.", child_arg)
                    elif expr_type == Type.ERROR:
                        # Error already reported by expression visitor
                        pass
            elif isinstance(child_arg, TerminalNodeImpl) and child_arg.getSymbol().type == LittleDuckLexer.CTE_STR:
                pass # String literals are fine
            elif isinstance(child_arg, TerminalNodeImpl) and child_arg.getSymbol().type == LittleDuckLexer.COMMA:
                pass # Skip commas
            # else: # Should not happen if grammar for print_args is correct
                # self.add_error("Malformed argument in print statement.", child_arg)
        return None

    def visitCondition(self, ctx:LittleDuckParser.ConditionContext):
        self.visit(ctx.expression()) 
        if not self.operand_stack:
            self.add_error("Could not determine type of condition expression in IF statement.", ctx.expression())
        else:
            condition_type = self.operand_stack.pop()
            if condition_type not in [Type.BOOL, Type.INT, Type.ERROR]: 
                self.add_error(f"Condition expression in IF statement must be boolean or int, got '{condition_type.value}'.", ctx.expression())
        
        self.visit(ctx.body(0)) # Then body

        if ctx.ELSE(): 
            if len(ctx.body()) > 1: 
                 self.visit(ctx.body(1)) # Else body
            else: 
                 self.add_error("ELSE clause found but no corresponding body.", ctx.ELSE().getSymbol())
        return None

    def visitCycle(self, ctx:LittleDuckParser.CycleContext):
        self.visit(ctx.expression()) 
        if not self.operand_stack:
            self.add_error("Could not determine type of condition expression in WHILE statement.", ctx.expression())
        else:
            condition_type = self.operand_stack.pop()
            if condition_type not in [Type.BOOL, Type.INT, Type.ERROR]:
                self.add_error(f"Condition expression in WHILE statement must be boolean or int, got '{condition_type.value}'.", ctx.expression())

        self.visit(ctx.body()) 
        return None

    def visitF_call(self, ctx:LittleDuckParser.F_callContext):
        func_name_token = ctx.ID().getSymbol()
        func_name = func_name_token.text

        func_entry = self.symbol_table.get_function(func_name)
        if not func_entry:
            self.add_error(f"Function '{func_name}' not declared.", func_name_token)
            if ctx.expression_multiple():
                # Visit to pop any pushed types from operand_stack by expressions
                for expr_node in ctx.expression_multiple().expression():
                    self.visit(expr_node)
                    if self.operand_stack: self.operand_stack.pop()
            return None

        arg_types_from_call = []
        expr_multiple_ctx = ctx.expression_multiple()
        
        if expr_multiple_ctx:
            for expr_ctx in expr_multiple_ctx.expression():
                self.visit(expr_ctx)
                if not self.operand_stack:
                    self.add_error(f"Could not determine type of an argument for function '{func_name}'.", expr_ctx)
                    arg_types_from_call.append(Type.ERROR) 
                else:
                    arg_types_from_call.append(self.operand_stack.pop())
        
        if len(arg_types_from_call) != func_entry.param_count:
            self.add_error(f"Function '{func_name}' expects {func_entry.param_count} arguments, but got {len(arg_types_from_call)}.", func_name_token)
        else:
            for i in range(len(arg_types_from_call)):
                actual_arg_type = arg_types_from_call[i]
                expected_param_type = func_entry.param_types[i]
                
                if actual_arg_type == Type.ERROR: continue 

                # Using ASSIGN operator from semantic cube to check assign-compatibility
                if self.semantic_cube.get_type(expected_param_type, actual_arg_type, Operator.ASSIGN) == Type.ERROR:
                    param_name = func_entry.param_names[i] if i < len(func_entry.param_names) else f"#{i+1}"
                    arg_expr_node = expr_multiple_ctx.expression(i) if expr_multiple_ctx else func_name_token
                    self.add_error(f"Type mismatch for argument '{param_name}' of function '{func_name}'. Expected compatible with '{expected_param_type.value}', got '{actual_arg_type.value}'.", arg_expr_node)
        
        # f_call is a statement, its return type (if it were an expression) is not pushed to operand_stack here.
        # If LittleDuck allowed func calls in expressions, you'd push func_entry.return_type.
        return None

    def visitExpression_multiple(self, ctx:LittleDuckParser.Expression_multipleContext):
        # This rule is primarily a container. Its children (expressions) are visited by visitF_call.
        # No direct action needed here as part of the visitor flow, unless called standalone (which it isn't).
        return None
