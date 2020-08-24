from ast import *
from token import (Iter,Seperator,String,Number,Name,Operator,Keyword,Paren)
from expr import CallExpr

def parse(tokens):
    ast = AST()
    i = 0
    def walk():
        nonlocal i
        token = tokens[i]
        if token.type_ == Number.type_:
            i += 1
            return Number(token.value)
        elif token.type_ == String.type_:
            i += 1
            return String(token.value)
        if token.type_ == Name.type_:
            i += 1
            if tokens[i].type_ == Paren.type_ and \
                tokens[i].value == '(':
                callexpr = CallExpr(token)
                i += 1
                token = tokens[i]
                while token.type_ != Paren.type_ or \
                    (token.type_ == Paren.type_ and token.value != ')'):
                    if token.type_ == Seperator.type_:
                        i += 1
                        token = tokens[i]
                        continue
                    print(i, token, tokens[i])
                    callexpr.args.append(walk())
                    token = tokens[i]
                i += 1
                return callexpr
            else:
                return Name(token.value)
        else:
            raise SyntaxError(f'Could not parse token: "{token.value}" of type "{token.type_}"')

    while i < len(tokens):
        node = walk()
        ast.body.append(node)
    return ast