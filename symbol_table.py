# symbol_table.py

class VariableEntry:
    def __init__(self, name, type, address=None):
        self.name = name
        self.type = type
        self.address = address # For memory management in later stages

    def __str__(self):
        return f"Var: {self.name}, Type: {self.type.value if hasattr(self.type, 'value') else self.type}, Addr: {self.address}"

class FunctionEntry:
    def __init__(self, name, return_type, start_quad=None):
        self.name = name
        self.return_type = return_type
        self.param_types = [] # List of types of parameters
        self.param_names = [] # List of names of parameters
        self.variables = {}   # VariableTable for local variables (maps name to VariableEntry)
        self.param_count = 0
        self.local_var_count = 0 # Excluding params
        self.temp_var_count = 0 
        self.start_quad = start_quad

    def add_param(self, name, type):
        if name in self.param_names or name in self.variables:
            # self.add_error(f"Parameter '{name}' redeclared or conflicts with a local variable in function '{self.name}'.")
            return False # Indicate error
        
        self.param_types.append(type)
        self.param_names.append(name)
        self.param_count += 1
        self.variables[name] = VariableEntry(name, type) # Params are also local to the function
        return True

    def add_variable(self, name, type, address=None):
        if name in self.variables: # Checks params as well
            return False # Indicate error: redeclaration
        self.variables[name] = VariableEntry(name, type, address)
        self.local_var_count += 1
        return True # Indicate success

    def get_variable(self, name):
        return self.variables.get(name)

    def __str__(self):
        params_str = ", ".join([f"{p_name}:{p_type.value if hasattr(p_type, 'value') else p_type}" for p_name, p_type in zip(self.param_names, self.param_types)])
        # Filter out params from local vars for display if desired, or show all
        local_vars_only_str = "\n".join([f"\t{str(var)}" for var_name, var in self.variables.items() if var_name not in self.param_names])
        
        # Displaying params as part of local vars is also fine and simpler:
        all_local_vars_str = "\n".join([f"\t{str(var)}" for var in self.variables.values()])

        return_type_str = self.return_type.value if hasattr(self.return_type, 'value') else self.return_type
        return f"Func: {self.name}, Returns: {return_type_str}, Params: [{params_str}]\n  Local Vars (incl. params):\n{all_local_vars_str}"

class SymbolTable:
    def __init__(self):
        self.global_vars = {} 
        self.functions = {}   
        self.current_scope_name = 'global' # Tracks the name of the current scope ('global' or function name)

    def add_function(self, name, return_type):
        if name in self.functions:
            return None 
        func_entry = FunctionEntry(name, return_type)
        self.functions[name] = func_entry
        return func_entry

    def get_function(self, name):
        return self.functions.get(name)

    def add_global_variable(self, name, type, address=None):
        if name in self.global_vars:
            return False 
        self.global_vars[name] = VariableEntry(name, type, address)
        return True 

    def get_global_variable(self, name):
        return self.global_vars.get(name)

    def get_variable_in_scope(self, var_name, scope_name=None):
        # If scope_name is provided, use it. Otherwise, use self.current_scope_name.
        active_scope_name = scope_name if scope_name is not None else self.current_scope_name

        if active_scope_name and active_scope_name != 'global':
            current_func_entry = self.get_function(active_scope_name)
            if current_func_entry:
                var = current_func_entry.get_variable(var_name)
                if var:
                    return var
        
        return self.get_global_variable(var_name)

    def set_current_scope(self, scope_name):
        self.current_scope_name = scope_name

    def __str__(self):
        global_vars_str = "\n".join([f"  {str(var)}" for var in self.global_vars.values()])
        funcs_str = "\n".join([str(func) for func in self.functions.values()])
        return f"Symbol Table:\nGlobal Variables:\n{global_vars_str if global_vars_str else '  (none)'}\nFunctions:\n{funcs_str if funcs_str else '  (none)'}"

# Example Usage
if __name__ == '__main__':
    from semantic_cube import Type # Assuming Type enum is in semantic_cube

    st = SymbolTable()
    try:
        st.add_global_variable("count", Type.INT)
        st.add_global_variable("ratio", Type.FLOAT)
        
        main_func = st.add_function("main", Type.VOID)
        st.set_current_scope("main")
        if main_func:
            main_func.add_variable("x", Type.INT)

        process_func = st.add_function("process", Type.INT)
        if process_func:
            process_func.add_param("data", Type.INT)
            process_func.add_param("scale", Type.FLOAT)
            st.set_current_scope("process") # Set scope before adding local var to this func
            process_func.add_variable("result", Type.INT)

        print(st)

        st.set_current_scope("main")
        var_x = st.get_variable_in_scope("x")
        print(f"Found in main scope ('main'): x -> {var_x}")
        var_count = st.get_variable_in_scope("count")
        print(f"Found (global) in main scope ('main'): count -> {var_count}")

        st.set_current_scope("process")
        var_data = st.get_variable_in_scope("data") 
        print(f"Found in process scope ('process'): data -> {var_data}")
        var_result = st.get_variable_in_scope("result")
        print(f"Found in process scope ('process'): result -> {var_result}")
        var_ratio = st.get_variable_in_scope("ratio")
        print(f"Found (global) in process scope ('process'): ratio -> {var_ratio}")
        var_x_proc = st.get_variable_in_scope("x") 
        print(f"Found x in process scope ('process'): x -> {var_x_proc}")
        
        # Test get_variable_in_scope with explicit scope
        var_x_explicit = st.get_variable_in_scope("x", "main")
        print(f"Found x with explicit scope 'main': x -> {var_x_explicit}")


    except Exception as e:
        print(f"Error: {e}")
