import ast
import decimal

def NotInPrint(node, _nodemap):
    return None

def InPrint(node, _nodemap):
    return "in"

def IsNotPrint(node, _nodemap):
    return "!=="

def IsPrint(node, _nodemap):
    return "==="

def GtEPrint(node, _nodemap):
    return ">="

def GtPrint(node, _nodemap):
    return ">"

def LtEPrint(node, _nodemap):
    return "<="

def LtPrint(node, _nodemap):
    return "<"

def NotEqPrint(node, _nodemap):
    return "!="

def EqPrint(node, _nodemap):
    return "=="

def ComparePrint(node, _nodemap):
    left = generate_code(node.left)
    cmpstr = str(left)
    for i in range(len(node.comparators)):
        op, comp = generate_code(node.ops[i]), generate_code(node.comparators[i])
        if isinstance(node.ops[i], ast.In):
            cmpstr = f"{cmpstr} {op} {comp}"
        elif isinstance(node.ops[i], ast.NotIn):
            # get left comparator, slice left comparator out of str,
            # build str with previous compares and negated in compare
            leftcomp = cmpstr[cmpstr.rfind(" ") + 1:]
            cmpstr = cmpstr[:cmpstr.rfind(" ") + 1]
            cmpstr = f"{cmpstr} !({leftcomp} in {comp})"
        else:
            cmpstr = f"{cmpstr} {op} {comp}"
    return cmpstr

def AddPrint(node, _nodemap):
    return "+"

def SubPrint(node, _nodemap):
    return "-"

def MultPrint(node, _nodemap):
    return "*"

def DivPrint(node, _nodemap):
    return "/"

def FloorDivPrint(node, _nodemap):
    return "/"

def ModPrint(node, _nodemap):
    return "%"

def PowPrint(node, _nodemap):
    return None

def LShiftPrint(node, _nodemap):
    return "<<"

def RShiftPrint(node, _nodemap):
    return ">>"

def BitOrPrint(node, _nodemap):
    return "|"

def BitXorPrint(node, _nodemap):
    return "^"

def BitAndPrint(node, _nodemap):
    return "&"

def MatMultPrint(node, _nodemap):
    raise SyntaxError("Compiler does not support Matrix Multiplication Binary Operator '@'")

def BinOpPrint(node, _nodemap):
    left, op, right = generate_code(node.left), generate_code(node.op), generate_code(node.right)
    if isinstance(node.op, ast.Pow):
        return f"Math.pow({left}, {right})"
    elif isinstance(node.op, ast.FloorDiv):
        return f"Math.floor(({left}{op}{right}))"
    else:
        return f"{left}{op}{right}"

def NotPrint(node, _nodemap):
    return "!"

def UnaryOpPrint(node, _nodemap):
    return f"{generate_code(node.op)}{generate_code(node.operand)}"

def BoolOpPrint(node, _nodemap):
    left, right = [generate_code(node) for node in node.values]
    bool_ = generate_code(node.op)
    return f"{left} {bool_} {right}"

def OrPrint(node, _nodemap):
    return "||"

def AndPrint(node, _nodemap):
    return "&&"

def DictPrint(node, _nodemap):
    keys = [generate_code(el) for el in node.keys]
    values = [generate_code(el) for el in node.values]
    return dict(zip(keys, values))

def SetPrint(node, _nodemap):
    elts = ",".join(set(generate_code(el) for el in node.elts))
    return f"[{elts}]"

def ListPrint(node, _nodemap):
    elts = ",".join([generate_code(el) for el in node.elts])
    return f"[{elts}]"

def TuplePrint(node, _nodemap):
    elts = ",".join([str(generate_code(el)) for el in node.elts])
    return f"[{elts}]"

def NamePrint(node, _nodemap):
    return node.id

def FormattedValuePrint(node, _nodemap):
    return generate_code(node.value)

def ConstantPrint(node, _nodemap):
    numeric = (float, int, decimal.Decimal,)
    string = (str,)
    if type(node.value) in numeric:
        return node.value
    elif type(node.value) in string:
        return str(node.value)
    else:
        nameconstmap = {True: "true", False: "false", None: "null"}
        return nameconstmap[node.value]

def JoinedStrPrint(node, _nodemap):
    strval = ''
    for n in node.values:
        token = generate_code(n)
        strval += f'{token}' + '+'
    if strval[-1] == '+':
        strval = strval[:-1]
    return strval

def FunctionDefPrint(node, _nodemap):
    keyword = "function"
    name = node.name
    args = ','.join([arg.arg for arg in node.args.args])
    return f"{keyword} {name}({args}){{"

def AssignPrint(node, _nodemap):
    declare = "var"
    targets = ",".join([generate_code(target) for target in node.targets])
    value = generate_code(node.value)
    return f"{declare} {targets} = {value};"

_nodemap = {
    ast.FunctionDef: FunctionDefPrint,
    ast.JoinedStr: JoinedStrPrint,
    ast.Constant: ConstantPrint,
    ast.FormattedValue: FormattedValuePrint,
    ast.Name: NamePrint,
    ast.Assign: AssignPrint,
    ast.Tuple: TuplePrint,
    ast.Dict: DictPrint,
    ast.List: ListPrint,
    ast.Set: SetPrint,
    ast.BoolOp: BoolOpPrint,
    ast.Or: OrPrint,
    ast.And: AndPrint,
    ast.UnaryOp: UnaryOpPrint,
    ast.Not: NotPrint,
    ast.BinOp: BinOpPrint,
    ast.Add: AddPrint,
    ast.Sub: SubPrint,
    ast.Mult: MultPrint,
    ast.Div: DivPrint,
    ast.FloorDiv: FloorDivPrint,
    ast.Mod: ModPrint,
    ast.Pow: PowPrint,
    ast.LShift: LShiftPrint,
    ast.RShift: RShiftPrint,
    ast.BitOr: BitOrPrint,
    ast.BitXor: BitXorPrint,
    ast.BitAnd: BitAndPrint,
    ast.MatMult: MatMultPrint,
    ast.Compare: ComparePrint,
    ast.Eq: EqPrint,
    ast.NotEq: NotEqPrint,
    ast.Lt: LtPrint,
    ast.LtE: LtEPrint,
    ast.Gt: GtPrint,
    ast.GtE: GtEPrint,
    ast.Is: IsPrint,
    ast.IsNot: IsNotPrint,
    ast.In: InPrint,
    ast.NotIn: NotInPrint,
}
def generate_code(node):
    try:
        return _nodemap[type(node)](node, _nodemap)
    except KeyError:
        if isinstance(node, ast.Expr):
            return generate_code(node.value)
        else:
            return ''.join([generate_code(child) for child in node.body])

