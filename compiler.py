import sys
import ast
import os
import codegen

def pypile(infile):
    builddir = "build/"
    with open(infile, "rb") as file_:
        tree = ast.parse(file_.read())
        os.makedirs(os.path.dirname(builddir), exist_ok=True)
        jsscript = f"{builddir}{infile[:-3]}.js"
        with open(jsscript, "w") as newfile_:
            pymods_data = ""#codegen.generate_pymods()
            module = jsscript[jsscript.index("/") + 1:-3]
            data = codegen.generate_module(module, tree)
            newfile_.write(pymods_data + data)
    return
    #TODO implement visitors for things like; comprehensions (replace with For),Tuple (replace with Array or List), etc.
    """
    while True:
        try:
            expr = next(generator)
            trans = fns.get(type(expr))
            if trans:
                print(trans(expr))
        except StopIteration:
            print("Done Parsing :)")
            break
    """

pypile(sys.argv[1])

