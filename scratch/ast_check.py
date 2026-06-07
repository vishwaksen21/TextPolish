import ast
import sys

def check_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        return
        
    class NameChecker(ast.NodeVisitor):
        def __init__(self):
            self.defined = set()
            self.used = []
            
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                self.defined.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                self.used.append((node.id, node.lineno))
            self.generic_visit(node)
            
        def visit_FunctionDef(self, node):
            self.defined.add(node.name)
            # Add arguments
            for arg in node.args.args:
                self.defined.add(arg.arg)
            self.generic_visit(node)
            
        def visit_ClassDef(self, node):
            self.defined.add(node.name)
            self.generic_visit(node)
            
        def visit_Import(self, node):
            for alias in node.names:
                name = alias.asname or alias.name
                self.defined.add(name)
            self.generic_visit(node)
            
        def visit_ImportFrom(self, node):
            for alias in node.names:
                name = alias.asname or alias.name
                self.defined.add(name)
            self.generic_visit(node)

    checker = NameChecker()
    # Populate builtins
    import builtins
    checker.defined.update(dir(builtins))
    checker.defined.update(['__file__', '__name__', '__package__', '__doc__'])
    
    checker.visit(tree)
    
    # We do a simplified check for globals/locals.
    # Note that local variables inside functions won't be seen as globally defined, 
    # but we can look for obviously missing names.
    # Let's also check for name errors in the AST.
    print("AST Check complete. No syntax errors.")

if __name__ == '__main__':
    check_file('hotkeys.py')
