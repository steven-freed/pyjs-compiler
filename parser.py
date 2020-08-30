import sys
import ast
import codegen

def parse(infile, outfile):
    with open(infile, "rb") as file_:
        tree = ast.parse(file_.read())
        outfile = outfile if outfile.find(".js") > -1 else f"{outfile}.js"
        with open(outfile, "w") as newfile_:
            pymods_data = codegen.generate_pymods()
            data = codegen.generate_code(tree)
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
try:
    parse(sys.argv[1], sys.argv[2])
except IndexError:
    parse(sys.argv[1], "out.js")
