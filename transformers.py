import ast

class FunctionDefTrans(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        return FunctionDef(
            
        )
        return Subscript(
            value=Name(id='data', ctx=Load()),
            slice=Index(value=Constant(value=node.id)),
            ctx=node.ctx
        )
