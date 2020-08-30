def foo(x, y):
    if x == y:
        x += 1
    else:
        y **= 2
    return x if x >= y else y
