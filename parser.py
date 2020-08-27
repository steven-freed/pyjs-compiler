import sys
import ast

def parse(filename):
    with open(filename, "rb") as file_:
        tree = ast.parse(file_.read())
        newfile = open(f"{filename[:-3]}.js", "w")
        generate_code(newfile, tree)
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

def JoinedStrPrint(node):
    strval = ""
    for n in node.values:
        print(n, n.value)
        if isinstance(n, ast.Constant) and n.value != " ":
            strval += f"{n.value}+"
        elif isinstance(n, ast.FormattedValue):
            strval += f"{n.value.value}+"
    return strval[:-1]

def FunctionDefPrint(node):
    keyword = "function"
    name = node.name
    args = ','.join([arg.arg for arg in node.args.args])
    return f"{keyword} {name}({args}){{"


def generate_code(handle, node):
    codemap = {
        ast.FunctionDef: FunctionDefPrint,
        ast.JoinedStr: JoinedStrPrint,
    }
    try:
        strdata = codemap[type(node)](node)
        print(f"Wrote {strdata} to file")
        handle.write(strdata)       
    except KeyError:
        err = KeyError(f"Node of type '{type(node)}' does not exist")
        print(err)
        if isinstance(node, ast.Expr):
            generate_code(handle, node.value)
        elif isinstance(node, ast.Assign):
            [generate_code(handle, child) for child in node.targets]
        else:
            [generate_code(handle, child) for child in node.body]
    handle.close()

parse(sys.argv[1])

