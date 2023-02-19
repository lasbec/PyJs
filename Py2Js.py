import ast
import sys

def translate_py_to_js_file(file_in_path, verbose = False):
    file_out_path = ".".join(file_in_path.split(".")[0:-1]) + ".js"

    with open(file_in_path, "r") as f:
        fileLines = f.readlines()
        fileContent = "\n".join(fileLines)

    fileAst = ast.parse(fileContent)
    if(verbose):
        print("Py AST:\n", ast.dump(fileAst, indent=4))

    # to test we need to provied print function in javascript, so this is the first dirty approach
    js_file_content = "let print = console.log\n" + to_js(fileAst)


    with open(file_out_path, "w") as f:
        f.write(js_file_content)
        if(verbose):
            print("Write Js result to:",file_out_path)

    return file_out_path



def _to_js(cls):
    def inner_to_js(func):
        cls._to_js = func
        return func
    return inner_to_js

@_to_js(ast.Module)
def module_to_js(mod):
    return "\n".join(map(lambda c: to_js(c),mod.body))

@_to_js(ast.Pass)
def pass_to_js(passOp: ast.Pass):
    return ""

@_to_js(ast.Expr)
def expr_to_js(expr:ast.Expr):
    return to_js(expr.value)

@_to_js(ast.Call)
def expr_to_js(call:ast.Call):
    assert len(call.keywords) == 0
    return (to_js(call.func) 
        + "("
        + ",".join(map(lambda c : to_js(c),call.args))
        + ");"
    )

@_to_js(ast.Assign)
def assign_to_js(assignment: ast.Assign):
    assert len(assignment.targets) == 1
    return (
        "let "
        +
        to_js(assignment.targets[0])
        + 
        " = "
        +
        to_js(assignment.value)
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
        return f"{const.value}"
    elif(valType == int):
        return f"{const.value}"
    elif(valType == bool):
        return "true" if const.value else "false"
    elif(valType == str):
        return '"' + const.value + '"'
    raise Exception(f"constant not implemented for {valType}.")

@_to_js(ast.List)
def list_to_js(lst: ast.List):
    return "[" + ",".join(map(lambda c: to_js(c), lst.elts)) + "]"

@_to_js(ast.UnaryOp)
def bin_op_to_js(op: ast.UnaryOp):
    op_str = operator_to_str_map[type(op.op)]
    assert op_str != None
    return f"({op_str} {to_js(op.operand)})"

@_to_js(ast.BinOp)
def bin_op_to_js(op: ast.BinOp):
    op_str = operator_to_str_map[type(op.op)]
    assert op_str != None
    return f"{to_js(op.left)} {op_str} {to_js(op.right)}"

operator_to_str_map = {
    ast.Del: None,
    ast.Load: None,
    ast.Store: None,
    ast.And: "&&",
    ast.Or: "||",
    ast.Add: "+",
    ast.BitAnd: "&",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.Div: None,
    ast.FloorDiv: None,
    ast.Mod: "%",
    ast.Mult: "*",
    ast.MatMult: None,
    ast.Pow: "**",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.Sub: "-",

    ast.Invert: None,
    ast.Not: "!",
    ast.UAdd: None,
    ast.USub: None,
    ast.cmpop: None,
    ast.Eq: None,
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.In: None,
    ast.Is: "===",
    ast.IsNot: "!==",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.NotEq: None,
    ast.NotIn: None,
}

operator_to_py_method_map = {
    ast.Del: None,
    ast.Load: None,
    ast.Store: None,
    ast.And: None,
    ast.Or: None,
    ast.Add: "__add__",
    ast.BitAnd: "__and__",
    ast.BitOr: "__or__",
    ast.BitXor: "__xor__",
    ast.Div: None,
    ast.FloorDiv: None,
    ast.LShift: None,
    ast.Mod: "__mod__",
    ast.Mult: "__mult__",
    ast.MatMult: None,
    ast.Pow: None,
    ast.RShift: None,
    ast.Sub: "__sub__",

    ast.Invert: "__invert__",
    ast.Not: None,
    ast.UAdd: None,
    ast.USub: None,
    ast.cmpop: None,
    ast.Eq: None,
    ast.Gt: "__gt__",
    ast.GtE: "__ge__",
    ast.In: None,
    ast.Is: None,
    ast.IsNot: None,
    ast.Lt: "__lt__",
    ast.LtE: "__le__",
    ast.NotEq: "__ne__",
    ast.NotIn: None,
}


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
        +  "\n".join(map(lambda c: to_js(c), funDef.body)) 
        + "\n}"
        )

def to_js(pyAst):
    return pyAst.__class__._to_js(pyAst)


if (__name__ == "__main__"):
    translate_py_to_js_file(sys.argv[1], True)