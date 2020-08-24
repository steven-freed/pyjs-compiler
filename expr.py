class CallExpr:
    type_ = 'CALL_EXPR'
    def __init__(self, name, args=[]):
        self.name = name
        self.args = args
    def __str__(self):
        return f"{self.type_}: {self.name}{tuple([str(arg) for arg in self.args])}"