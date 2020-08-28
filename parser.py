import sys
import ast
import codegen

def parse(filename):
    with open(filename, "rb") as file_:
        tree = ast.parse(file_.read())
        with open(f"{filename[:-3]}.js", "w") as newfile_:
            data = codegen.generate_code(tree)
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

parse(sys.argv[1])

