import toks
import tokenize
#from parser import *
import sys

def lexify(filename):
    tokens = []
    f = open(filename, "rb")
    tokgen = tokenize.tokenize(f.readline)
    while True:
        try:
            token = next(tokgen)
            if token.type is toks.token.ERRORTOKEN:
                raise SyntaxError(f'Invalid token on line {token.start[0]}: "{token.line}"')
            tokens.append(toks.Token(toks.tokens[token.type], token.string))
        except StopIteration:
            print(*[str(t) for t in tokens])
            return
    printtoks(tokens)
    ast = parse(tokens)
    print(ast.body[0])
    f.close()

def printtoks(tokens):
    for token in tokens:
        print(token)

lexify(sys.argv[1])
