import sys
import ast

def parse(filename):
    with open(filename, "rb") as file_:
        tree = ast.parse(file_.read())
        newfile = open(f"{filename[:-3]}.js", "w")
        generate_code(newfile, tree)
        #generator = ast.walk(tree)
    return#TODO
    while True:
        try:
            expr = next(generator)
            trans = fns.get(type(expr))
            if trans:
                print(trans(expr))
        except StopIteration:
            print("Done Parsing :)")
            break

def FunctionDefPrint(node):
    keyword = "function"
    name = node.name
    args = ','.join([arg.arg for arg in node.args.args])
    return f"{keyword} {name}({args}){{"

def generate_code(handle, node):
    codemap = {
        ast.FunctionDef: FunctionDefPrint,
    }
    try:
        strdata = codemap[type(node)](node)
        print(f"Wrote {strdata} to file")
        handle.write(strdata)       
    except KeyError:
        err = KeyError(f"Node of type '{type(node)}' does not exist")
        print(err)
        [generate_code(handle, child) for child in node.body]
    handle.close()

parse(sys.argv[1])

