import ast
import sys

fileInPath = sys.argv[1]
fileOutPath = ".".join(fileInPath.split(".")[0:-1]) + ".js"
print(f"Reading {fileInPath}.")

with open(fileInPath, "r") as f:
    fileLines = f.readlines()
    print(f"Read {len(fileLines)} lines.")
    fileContent = "\n".join(fileLines)


fileAst = ast.parse(fileContent)


def _to_js(cls):
    def inner_to_js(func):
        cls._to_js = func
        return func
    return inner_to_js

@_to_js(ast.Module)
def module_to_js(mod):
    return "\n".join(map(lambda c: py_ast_to_js(c),mod.body))

@_to_js(ast.Pass)
def pass_to_js(passOp):
    return ""

@_to_js(ast.Assign)
def assign_to_js(assignment: ast.Assign):
    assert len(assignment.targets) == 1
    return (
        "let "
        +
        py_ast_to_js(assignment.targets[0])
        + 
        " = "
        +
        py_ast_to_js(assignment.value)
        + 
        ";"
    )

@_to_js(ast.Name)
def assign_to_js(name: ast.Name):
    return name.id

@_to_js(ast.Constant)
def constant_to_js(const: ast.Constant):
    valType = type(const.value)
    if(valType == float):
        return const.value
    elif(valType == int):
        return f"{const.value}n"
    elif(valType == bool):
        return "true" if const.value else "false"
    elif(valType == str):
        return '"' + const.value + '"'
    raise Exception(f"constant not implemented for {valType}.")

@_to_js(ast.FunctionDef)
def function_def_to_js(funDef: ast.FunctionDef):
    assert len(funDef.decorator_list) == 0
    args = funDef.args
    assert len(args.posonlyargs) == 0
    assert len(args.kwonlyargs) == 0
    assert len(args.kw_defaults) == 0
    assert len(args.defaults) == 0

    
    return ("function "
        + funDef.name 
        + "("
        + ",".join(map(lambda a: a.arg, args.args))
        + "){\n" 
        +  "\n".join(map(lambda c: py_ast_to_js(c), funDef.body)) 
        + "\n}"
        )

def py_ast_to_js(pyAst):
    return pyAst.__class__._to_js(pyAst)


print(ast.dump(fileAst, indent=4))

print("-----------\n\n\n", py_ast_to_js(fileAst))