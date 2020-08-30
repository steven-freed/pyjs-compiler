try:
    print("hi")
except TypeError as te:
    raise te
finally:
    x += 3
    print("done")
