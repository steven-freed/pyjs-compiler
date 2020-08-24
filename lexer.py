from token import *
from parser import *
import sys

def lexify(filename):
    f = open(filename)
    tokens = []
    while True:
        buf = f.readline()
        i, j = 0, len(buf) - 1
        if not buf: break
        while i <= j:
            token = buf[i]
            if token in Token.NULL:
               pass
            elif token in Token.SEPERATOR:
                tokens.append(Seperator(token))
            elif token in Token.PAREN:
                tokens.append(Paren(token))
            elif token in Token.ITER:
                tokens.append(Iter(token))
            elif token in Token.OPERATOR:
                op = buf[i]
                i += 1
                while buf[i] in Token.OPERATOR:
                    op = f'{op}{buf[i]}'
                    i += 1
                tokens.append(Operator(op))
                continue
            elif token in Token.STRING:
                string = buf[i]
                i += 1
                while buf[i] != token:
                    string = f'{string}{buf[i]}' 
                    i += 1
                string = f'{string}{buf[i]}' 
                i += 1
                tokens.append(String(string))
                continue
            elif token in Token.NUMBER:
                num = buf[i]
                i += 1
                while buf[i].isnumeric() or buf[i] == '.':
                    num = f'{num}{buf[i]}' 
                    i += 1
                tokens.append(Number(num))
                continue
            elif token.isalpha():
                name = buf[i]
                i += 1
                while buf[i].isalpha():
                    name = f'{name}{buf[i]}' 
                    i += 1
                if name in Token.KEYWORD:
                    tokens.append(Keyword(name))
                elif name in Token.OPERATOR:
                    tokens.append(Operator(name))
                else:
                    tokens.append(Name(name))
                continue
            else:
                raise ValueError(f'Token "{token}" not recognized')
            i += 1
    printtoks(tokens)
    ast = parse(tokens)
    print(ast.body[0])
    f.close()

def printtoks(tokens):
    for token in tokens:
        print(token)

lexify(sys.argv[1])
