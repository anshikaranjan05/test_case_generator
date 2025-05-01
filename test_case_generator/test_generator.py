import ast
import os

def parse_python_file(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            functions.append({'name': node.name, 'args': args})
    return functions

def generate_test_case(func):
    test_code = f"def test_{func['name']}():\n"
    arg_string = ", ".join("0" for _ in func['args'])  # dummy values
    test_code += f"    result = {func['name']}({arg_string})\n"
    test_code += f"    assert result is not None  # Replace with actual expected output\n"
    return test_code

def create_test_file(source_file, output_file='test_generated.py'):
    functions = parse_python_file(source_file)
    with open(output_file, 'w') as f:
        f.write("import pytest\n")
        f.write(f"from {os.path.splitext(os.path.basename(source_file))[0]} import *\n\n")
        for func in functions:
            f.write(generate_test_case(func))
            f.write("\n\n")
    print(f"Test cases generated in {output_file}")

# Example usage:
# create_test_file('sample_code.py')
