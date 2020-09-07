import sys
import ast
import os
import codegen

INDEX = """
<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no"/>
        <title>My App</title>
        <script src="{build}"></script>
    </head>
    <body>
        <h1>Thanks for using Python-JavaScript Compiler :)</h1>
    </body>
</html>
"""

def pypile(infile):
    builddir = "build/"
    with open(infile, "rb") as file_:
        tree = ast.parse(file_.read())
        os.makedirs(os.path.dirname(builddir), exist_ok=True)
        jsscript = f"{infile[:-3]}.js"
        with open(f"{builddir}{jsscript}", "w") as newfile_:
            pymods_data = ""#codegen.generate_pymods()
            module = jsscript[:-3]
            data = codegen.generate_module(module, tree)
            newfile_.write(pymods_data + data)
        with open(f"{builddir}index.html", "w") as index:
            index.write(INDEX.format(build=jsscript))
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

