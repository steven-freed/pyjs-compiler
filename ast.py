class AST:
    def __init__(self, body=[]):
        self.type_ = 'PROGRAM'
        self.body = body

    def __str__(self):
        return f'{self.type_}={self.body}'