import sys
import decimal
import ast

def parse(filename):
    with open(filename, "rb") as file_:
        tree = ast.parse(file_.read())
        with open(f"{filename[:-3]}.js", "w") as newfile_:
            data = generate_code(tree)
            newfile_.write(data)
        #generator = ast.walk(tree)
    return#TODO implement visitors for things like; comprehensions (replace with For),Tuple (replace with Array or List), etc.
    while True:
        try:
            expr = next(generator)
            trans = fns.get(type(expr))
            if trans:
                print(trans(expr))
        except StopIteration:
            print("Done Parsing :)")
            break

def BoolOpPrint(node, codemap):
    left, right = [generate_code(node) for node in node.values]
    bool_ = generate_code(node.op)
    return f"{left} {bool_} {right}"

def OrPrint(node, codemap):
    return "||"

def AndPrint(node, codemap):
    return "&&"

def DictPrint(node, codemap):
    keys = [generate_code(el) for el in node.keys]
    values = [generate_code(el) for el in node.values]
    return dict(zip(keys, values))

def SetPrint(node, codemap):
    elts = ",".join(set(generate_code(el) for el in node.elts))
    return f"[{elts}]"

def ListPrint(node, codemap):
    elts = ",".join([generate_code(el) for el in node.elts])
    return f"[{elts}]"

def TuplePrint(node, codemap):
    # TODO fix for Assign Node
    elts = ",".join(tuple(generate_code(el) for el in node.elts))
    return f"[{elts}]"

def NamePrint(node, codemap):
    return node.id

def FormattedValuePrint(node, codemap):
    return generate_code(node.value)

def ConstantPrint(node, codemap):
    numeric = (float, int, decimal.Decimal,)
    string = (str,)
    if type(node.value) in numeric:
        return node.value
    elif type(node.value) in string:
        return str(node.value)
    else:
        nameconstmap = {True: "true", False: "false", None: "null"}
        return nameconstmap[node.value]

def JoinedStrPrint(node, codemap):
    strval = ''
    for n in node.values:
        token = generate_code(n)
        strval += f'{token}' + '+'
    if strval[-1] == '+':
        strval = strval[:-1]
    return strval

def FunctionDefPrint(node, codemap):
    keyword = "function"
    name = node.name
    args = ','.join([arg.arg for arg in node.args.args])
    return f"{keyword} {name}({args}){{"

def AssignPrint(node, codemap):
    declare = "var"
    targets = ",".join([generate_code(target) for target in node.targets])
    value = generate_code(node.value)
    return f"{declare} {targets} = {value};"

def generate_code(node):
    codemap = {
        ast.FunctionDef: FunctionDefPrint,
        ast.JoinedStr: JoinedStrPrint,
        ast.Constant: ConstantPrint,
        ast.FormattedValue: FormattedValuePrint,
        ast.Name: NamePrint,
        ast.Assign: AssignPrint,
        ast.Tuple: TuplePrint,
        ast.Dict: DictPrint,
        ast.List: ListPrint,
        ast.Set: SetPrint,
        ast.BoolOp: BoolOpPrint,
        ast.Or: OrPrint,
        ast.And: AndPrint,
    }
    try:
        return codemap[type(node)](node, codemap)
    except KeyError:
        if isinstance(node, ast.Expr):
            return generate_code(node.value)
        else:
            return ''.join([generate_code(child) for child in node.body])

parse(sys.argv[1])

