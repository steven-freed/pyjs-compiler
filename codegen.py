import ast
import decimal
from collections.abc import Iterable

#TODO
"""
- implement imports: make python modules using es3 js module pattern
- implement builtins/exc: make map of builtins and exceptions to js
"""
GLOBALS = set()

def SubscriptPrint(node, nodemap):
    value, slice_ = generate_code(node.value), generate_code(node.slice)
    return f"{value}{slice_}"

def ExtSlicePrint(node, nodemap):
    raise SyntaxError("Complex slicing is not supported by JavaScript")

def SlicePrint(node, nodemap):
    if node.step: raise SyntaxError("Slicing by step is not supported by JavaScript")
    l = generate_code(node.lower) if node.lower else 0
    u = generate_code(node.upper) if node.upper else None
    if not u:
        return f".slice({l})"
    else:
        return f".slice({l},{u})"

def IndexPrint(node, nodemap):
    value = generate_code(node.value)
    return f"[{value}]"

def AttributePrint(node, nodemap):
    # TODO replace append with push, remove with pop, etc.
    value = generate_code(node.value)
    return f"{value}.{node.attr}"

def IfExpPrint(node, nodemap):
    ifexpr = generate_code(node.test)
    body, orelse = generate_code(node.body), generate_code(node.orelse)
    return f"{ifexpr} ? {body}:{orelse};"    

def StarredPrint(node, nodemap):
    raise SyntaxError("JavaScript does not support packing or unpacking")

def DeletePrint(node, nodemap):
    targets = ",".join([str(generate_code(t)) for t in node.targets])
    return f"delete {targets};"

def CallPrint(node, nodemap):
    func = generate_code(node.func)
    callstr = f"{func}("
    for i in range(len(node.args)):
        arg = generate_code(node.args[i])
        if i == len(node.args) - 1:
            callstr = f"{callstr}{arg}"
        else:
            callstr = f"{callstr}{arg},"
    callstr = f"{callstr});"
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
    elts = ",".join([str(generate_code(el)) for el in node.elts])
    return f"[{elts}]"

def TuplePrint(node, nodemap):
    elts = ",".join([str(generate_code(el)) for el in node.elts])
    return f"[{elts}]"

def NamePrint(node, nodemap):
    context = ("self", "this")
    return node.id if node.id.find(context[0]) < 0 else context[1] 

def FormattedValuePrint(node, nodemap):
    return generate_code(node.value)

def ConstantPrint(node, nodemap):
    numeric = (float, int, decimal.Decimal,)
    string = (str,)
    if type(node.value) in numeric:
        return node.value
    elif type(node.value) in string:
        return f'"{node.value}"'
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

def ReturnPrint(node, nodemap):
    return f"return {generate_code(node.value)};"

def FunctionDefPrint(node, nodemap):
    name = getattr(node, "name", "")
    args = generate_code(node.args)
    fn = f"function {name}({args}){{"
    if isinstance(node.body, Iterable):
        fnbody = "".join([str(generate_code(node)) for node in node.body])
        retstr = generate_code(node.returns)
        fn += f"{fnbody}{retstr}}}"
    else:
        fn += f"return {str(generate_code(node.body))}}}"
    return fn

def LambdaPrint(node, nodemap):
    return FunctionDefPrint(node, nodemap)

def AssignPrint(node, nodemap):
    asnstr = "var " if isinstance(node.targets[0], ast.Name) else ""
    if len(getattr(node.value, "elts", [])) == len(getattr(node.targets[0], "elts", [None])):
        for i in range(len(node.value.elts)):
            target, val = generate_code(node.targets[0].elts[i]), generate_code(node.value.elts[i])    
            if (i + 1) == len(node.value.elts):
                asnstr += f"{target}={val};"
            else:
                asnstr += f"{target}={val},"
    else:
        isiter = False
        for n in node.targets:
            if isinstance(n, ast.List) or isinstance(n, ast.Tuple):
                isiter = True
                break
        if not isiter:
            target, val = generate_code(node.targets[0]), generate_code(node.value)
            asnstr += f"{target}={val};"
        else:
            raise SyntaxError("Unpacking is not currently supported")
    if asnstr.find("this") > -1:
        asnstr = asnstr.replace("var", "")
    return asnstr

def AugAssignPrint(node, nodemap):
    target, op, value = generate_code(node.target), generate_code(node.op), generate_code(node.value)
    if isinstance(node.op, ast.Pow):
        return f"{target} = Math.pow({target}, {value});"
    elif isinstance(node.op, ast.FloorDiv):
        return f"{target} = Math.floor(({target}{op}{value}));"
    else:
        return f"{target}{op}={value};"

def RaisePrint(node, nodemap):
    throwstr = "throw "
    if node.exc:
        exc = generate_code(node.exc)
        throwstr += f"{exc};"
    else:
        throwstr += "_;"
    return throwstr

def AssertPrint(node, nodemap):
    # allows client to make assertions without effecting js 
    return ""

def PassPrint(node, nodemap):
    # allows client to make passes without effecting js
    return ""

def BreakPrint(node, nodemap):
    return "break;"

def ContinuePrint(node, nodemap):
    return "continue;"

def IfPrint(node, nodemap):
    cmptest = generate_code(node.test)
    ifstr = f"if({cmptest}){{"
    ifbody = "".join([str(generate_code(node)) for node in node.body])
    ifstr = f"{ifstr}{ifbody}}}"
    if isinstance(node.orelse[0], ast.If): # If nodes for orelse = elif
        elifstr = "".join([str(IfPrint(node, nodemap)) for node in node.orelse])
        ifstr = f"{ifstr}else {elifstr}"
    else: # else body of nodes
        elsebody = "".join([str(generate_code(node)) for node in node.orelse])
        ifstr = f"{ifstr}else{{{elsebody}}}"
    return ifstr

def WhilePrint(node, nodemap):
    cmptest = generate_code(node.test)
    whilebody = "".join([generate_code(node) for node in node.body])
    return f"while({cmptest}){{{whilebody}}}"

def ForPrint(node, nodemap):
    iter_ = generate_code(node.iter)
    range_, enum_ = None, None
    if iter_.find("range(") > -1:
        range_ = eval(iter_[:-1])
    target = generate_code(node.target)
    if range_:
        forstr = f"for(var {target}={range_.start};{target}<{range_.stop};{target}+={range_.step}){{"
    else:
        forstr = f"for(var {target} in {iter_}){{{target} = {iter_}[{target}];"
    forbody = "".join([str(generate_code(node)) for node in node.body])
    forstr += f"{forbody}}}"
    return forstr

def withitemPrint(node, nodemap):
    withitemstr = ""
    name, alias = generate_code(node.context_expr), None
    if node.optional_vars:
        alias = generate_code(node.optional_vars)
        withitemstr = f"var {alias} = {name}"
    withitemstr = f"{withitemstr}{alias or name}.__enter__();"
    return withitemstr

def WithPrint(node, nodemap):
    def withitemAlias(node):
        name = None
        if node.optional_vars:
            name = generate_code(node.optional_vars)
        else:
            name = generate_code(node.context_expr)
        return name
    itemaliases = [withitemAlias(node) for node in node.items]
    exitmethods = "".join([f"{alias}.__exit__(null, null, null);" for alias in itemaliases])
    items = "".join([str(withitemPrint(node, nodemap)) for node in node.items])
    withbody = "".join([str(generate_code(node)) for node in node.body])
    return f"{items}{withbody}{exitmethods}"

def TryPrint(node, nodemap):
    trystr = "try{"
    trybody = "".join([str(generate_code(node)) for node in node.body])
    trystr += f"{trybody}}}"
    if len(node.handlers) > 1:
        raise SyntaxError(f"JavaScript only allows for a single handler, you have {len(node.handlers)} handlers")
    handler = generate_code(node.handlers[0])
    trystr += f"{handler}finally{{"
    finalbody = "".join([str(generate_code(node)) for node in node.finalbody])
    trystr += f"{finalbody}}}"
    return trystr

def ExceptHandlerPrint(node, nodemap):
    catchstr = f"catch({node.name or '_'}){{"
    catchbody = ""
    for n in node.body:
        nodestr = generate_code(n)
        catchbody += nodestr
    catchstr += f"{catchbody}}}"
    return catchstr

def argumentsPrint(node, nodemap):
    # TODO fix kwargs, add if checks for null arg and put default
    args = ','.join([arg.arg for arg in node.args if arg.arg != "self"])
    return args

def argPrint(node, nodemap):
    return str(node.arg)

def YieldPrint(node, nodemap):
    raise SyntaxError("Yield not supported")

def YieldFromPrint(node, nodemap):
    raise SyntaxError("YieldFrom not supported")

def NonlocalPrint(node, nodemap):
    return ""

def GlobalPrint(node, nodemap):
    # add to globals for js module pattern
    return ""

def ClassDefPrint(node, nodemap):
    bases = [generate_code(base) for base in node.bases]
    classdef = {'name': node.name, 'bases': [bases], 'body': {'fns': {}, 'static': {}}}
    for propnode in node.body:
        if isinstance(propnode, ast.FunctionDef):
            name = propnode.name
            classdef['body']['fns'][name] = generate_code(propnode)
        elif isinstance(propnode, ast.Assign):
            name = propnode.targets[0].id
            value = generate_code(propnode)
            classdef['body']['static'][name] = value[value.index("=") + 1]
        else:
            raise SyntaxError(f'ClassDef node "{propnode}" not recognized')
    classstr = classdef['body']['fns']['__init__'].replace('__init__', classdef["name"])
    del classdef["body"]['fns']["__init__"]
    for type_ in classdef["body"]:
        for k, v in classdef["body"][type_].items():
            if type_ == 'fns':
                classstr += f"{classdef['name']}.prototype.{k}={v};" 
            elif type_ == 'static':
                classstr += f"{classdef['name']}.{k}={v};" 
    return classstr

_nodemap = {
    type(None): lambda a,b:"",
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
    ast.Delete: DeletePrint,
    ast.IfExp: IfExpPrint,
    ast.Attribute: AttributePrint,
    ast.Subscript: SubscriptPrint,
    ast.Index: IndexPrint,
    ast.Slice: SlicePrint,
    ast.ExtSlice: ExtSlicePrint,
    ast.Starred: StarredPrint,
    ast.AugAssign: AugAssignPrint,
    ast.Raise: RaisePrint,
    ast.Assert: AssertPrint,
    ast.Pass: PassPrint,
    ast.If: IfPrint,
    ast.Break: BreakPrint,
    ast.Continue: ContinuePrint,
    ast.While: WhilePrint,
    ast.For: ForPrint,
    ast.withitem: withitemPrint,
    ast.With: WithPrint,
    ast.Try: TryPrint,
    ast.ExceptHandler: ExceptHandlerPrint,
    ast.Return: ReturnPrint,
    ast.Lambda: LambdaPrint,
    ast.arguments: argumentsPrint,
    ast.arg: argPrint,
    ast.Yield: YieldPrint,
    ast.YieldFrom: YieldFromPrint,
    ast.Nonlocal: NonlocalPrint,
    ast.Global: GlobalPrint,
    ast.ClassDef: ClassDefPrint,
}
def generate_code(node):
    try:
        return _nodemap[type(node)](node, _nodemap)
    except KeyError:
        if isinstance(node, ast.Expr):
            return _nodemap[type(node.value)](node.value, _nodemap)
        elif isinstance(node, ast.Module):
            mod = ""
            for child in node.body:
                if getattr(child, "name", False):
                    GLOBALS.add(child.name)
                elif getattr(child, "targets", False):
                    if getattr(child.targets[0], "elts", False):
                        [GLOBALS.add(el.id) for target in child.targets for el in target.elts]
                    else:
                        [GLOBALS.add(target.id) for target in child.targets]
                mod += generate_code(child)
            return mod 
        else:
            raise SyntaxError(f"Type {type(node)} not supported by JavaScript or already has built in functionality")

def generate_module(module, tree):
    data = f"var {module} = (function(){{"
    data += generate_code(tree)
    data += f"return {{"
    for i, gvar in enumerate(GLOBALS):
        if (i + 1) == len(GLOBALS):
            data += f"'{gvar}':{gvar}"
        else:
            data += f"'{gvar}':{gvar},"
    data += "}})();"
    return data

def generate_pymods():
    with open("pymods/__builtins__.js", "r") as f:
        return f.read()
