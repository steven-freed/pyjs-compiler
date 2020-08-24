class Token:
    type_ = None
    SEPERATOR = (',', ';', ':', '.')
    PAREN = (')', '(')
    NULL = (' ', '\n', '\0', '\r', '\t', '#')
    STRING = ('"', "'")
    ITER = ('[', ']', '{', '}')
    NUMBER = tuple([str(i) for i in range(0, 10)])
    OPERATOR = ('+','-','+','*','/','and','not','or','is','in','%','!','=')
    KEYWORD = ('import','with','if','while','def','else','return', 'break', 'continue'
            'for','elif','yield','True','False','try','except','nonlocal','global','lambda')

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f'{self.type_}={self.value}'


class Iter(Token):
    type_ = 'iter'
    def __init__(self, value):
        super().__init__(value)

class Seperator(Token):
    type_ = 'seperator'
    def __init__(self, value):
        super().__init__(value)

class Paren(Token):
    type_ = 'paren'
    def __init__(self, value):
        super().__init__(value)

class String(Token):
    type_ = 'str'
    def __init__(self, value):
        super().__init__(value)

class Name(Token):
    type_ = 'name'
    def __init__(self, value):
        super().__init__(value)

class Number(Token):
    type_ = 'number'
    def __init__(self, value):
        super().__init__(value)

class Operator(Token):
    type_ = 'operator'
    def __init__(self, value, left=None, right=None):
        super().__init__(value)
        self.left = left
        self.right = right

class Keyword(Token):
    type_ = 'keyword'
    def __init__(self, value):
        super().__init__(value)
