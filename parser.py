import sys
import ast
import codegen

def parse(infile):
    with open(infile, "rb") as file_:
        tree = ast.parse(file_.read())
        jsscript = f"{infile[:-3]}.js"
        with open(jsscript, "w") as newfile_:
            pymods_data = ""#codegen.generate_pymods()
            module = jsscript[:-3]
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

parse(sys.argv[1])

