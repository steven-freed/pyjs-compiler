import ast
import decimal

def CallPrint(node, nodemap):
    func = generate_code(node.func)
    callstr = f"{func}("
    for arg in node.args:
        arg = generate_code(arg)
        callstr = f"{callstr}{arg},"
    kwargdict = "{"
    for kwarg in node.keywords:
        kwarg = generate_code(kwarg)
        kwargdict = f"{kwargdict}{kwarg},"
    if kwargdict != "{":
        kwargdict = f"{kwargdict[:-1]}}}"
        callstr = f"{callstr}{kwargdict});"
    else:
        callstr = f"{callstr[:-1]});"
    return callstr

def keywordPrint(node, nodemap):
    value = generate_code(node.value)
    return f"'{node.arg}':{value}"

def NotInPrint(node, nodemap):
    return None

def InPrint(node, nodemap):
    return "in"

def IsNotPrint(node, nodemap):
    return "!=="

def IsPrint(node, nodemap):
    return "==="

def GtEPrint(node, nodemap):
    return ">="

def GtPrint(node, nodemap):
    return ">"

def LtEPrint(node, nodemap):
    return "<="

def LtPrint(node, nodemap):
    return "<"

def NotEqPrint(node, nodemap):
    return "!="

def EqPrint(node, nodemap):
    return "=="

def ComparePrint(node, nodemap):
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

def AddPrint(node, nodemap):
    return "+"

def SubPrint(node, nodemap):
    return "-"

def MultPrint(node, nodemap):
    return "*"

def DivPrint(node, nodemap):
    return "/"

def FloorDivPrint(node, nodemap):
    return "/"

def ModPrint(node, nodemap):
    return "%"

def PowPrint(node, nodemap):
    return None

def LShiftPrint(node, nodemap):
    return "<<"

def RShiftPrint(node, nodemap):
    return ">>"

def BitOrPrint(node, nodemap):
    return "|"

def BitXorPrint(node, nodemap):
    return "^"

def BitAndPrint(node, nodemap):
    return "&"

def MatMultPrint(node, nodemap):
    raise SyntaxError("Compiler does not support Matrix Multiplication Binary Operator '@'")

def BinOpPrint(node, nodemap):
    left, op, right = generate_code(node.left), generate_code(node.op), generate_code(node.right)
    if isinstance(node.op, ast.Pow):
        return f"Math.pow({left}, {right})"
    elif isinstance(node.op, ast.FloorDiv):
        return f"Math.floor(({left}{op}{right}))"
    else:
        return f"{left}{op}{right}"

def NotPrint(node, nodemap):
    return "!"

def UnaryOpPrint(node, nodemap):
    return f"{generate_code(node.op)}{generate_code(node.operand)}"

def BoolOpPrint(node, nodemap):
    left, right = [generate_code(node) for node in node.values]
    bool_ = generate_code(node.op)
    return f"{left} {bool_} {right}"

def OrPrint(node, nodemap):
    return "||"

def AndPrint(node, nodemap):
    return "&&"

def DictPrint(node, nodemap):
    keys = [generate_code(el) for el in node.keys]
    values = [generate_code(el) for el in node.values]
    return dict(zip(keys, values))

def SetPrint(node, nodemap):
    elts = ",".join(set(generate_code(el) for el in node.elts))
    return f"[{elts}]"

def ListPrint(node, nodemap):
    elts = ",".join([generate_code(el) for el in node.elts])
    return f"[{elts}]"

def TuplePrint(node, nodemap):
    elts = ",".join([str(generate_code(el)) for el in node.elts])
    return f"[{elts}]"

def NamePrint(node, nodemap):
    return node.id

def FormattedValuePrint(node, nodemap):
    return generate_code(node.value)

def ConstantPrint(node, nodemap):
    numeric = (float, int, decimal.Decimal,)
    string = (str,)
    if type(node.value) in numeric:
        return node.value
    elif type(node.value) in string:
        return str(node.value)
    else:
        nameconstmap = {True: "true", False: "false", None: "null"}
        return nameconstmap[node.value]

def JoinedStrPrint(node, nodemap):
    strval = ''
    for n in node.values:
        token = generate_code(n)
        strval += f'{token}' + '+'
    if strval[-1] == '+':
        strval = strval[:-1]
    return strval

def FunctionDefPrint(node, nodemap):
    keyword = "function"
    name = node.name
    args = ','.join([arg.arg for arg in node.args.args])
    return f"{keyword} {name}({args}){{"

def AssignPrint(node, nodemap):
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
    ast.Call: CallPrint,
    ast.keyword: keywordPrint,
}
def generate_code(node):
    try:
        return _nodemap[type(node)](node, _nodemap)
    except KeyError:
        if isinstance(node, ast.Expr):
            return _nodemap[type(node.value)](node.value, _nodemap)
        else:
            return ''.join([generate_code(child) for child in node.body])

