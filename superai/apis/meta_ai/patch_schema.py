"""Patches the schema file to add a new serialization method to the jsonb type"""
import ast

import astor

source_file_path = "meta_ai_graphql_schema.py"


class MethodInjector(ast.NodeTransformer):
    def visit_ClassDef(self, node):
        if node.name == "jsonb":
            method_exists = any(
                isinstance(child, ast.FunctionDef) and child.name == "__to_graphql_input__" for child in node.body
            )

            if not method_exists:
                method_code = """
@classmethod
def __to_graphql_input__(cls, value, *args, **kwargs):
    out = super().__to_graphql_input__(value, *args, **kwargs)
    if isinstance(value, dict):
        import re
        out = re.sub('(?<!: )"(\S*?)"', r"\\1", out)
    return out
"""
                method_ast = ast.parse(method_code).body
                node.body.extend(method_ast)

        return node


def add_method_if_not_exists(source_file_content):
    tree = ast.parse(source_file_content)
    MethodInjector().visit(tree)
    return astor.to_source(tree)


if __name__ == "__main__":
    with open(source_file_path, "r") as source_file:
        source_file_content = source_file.read()

    modified_file_content = add_method_if_not_exists(source_file_content)

    with open(source_file_path, "w") as source_file:
        source_file.write(modified_file_content)

    print("File updated successfully.")
