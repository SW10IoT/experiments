import ast
from pprint import pprint
file_name = 'example.py'

#obj = compile(open(file_name).read(), file_name, 'exec', ast.PyCF_ONLY_AST)
obj = ast.parse(open(file_name).read())


class Node:
    '''CFG Node'''
    def __init__(self, label,*,outgoing=list(), ingoing=list(), variables=list()):
        self.ingoing = ingoing
        self.outgoing = outgoing
        self.variables = variables
        self.label = label

    def __str__(self):
        return ' '.join(('Label: ',self.label, ' \toutgoing: \t', str([x.label for x in self.outgoing]), 'ingoing: ', str([x.label for x in self.ingoing]))) #' '.join(self.variables)))

CFG = list()

class Listener(ast.NodeVisitor):
    def visit_Assign(self, node):
        label = LabelVisitor()
        label.visit(node)

        vars = Vars()
        vars.visit(node)

        n = Node(label.result,variables=vars.result)
        CFG.append(n)
        return n
        #CFG.append((label.result, vars.result))


    def visit_While(self, node):
        test = self.visit(node.test)
        body = self.visit(node.body[0])
        if node.orelse:
            orelse = self.visit(node.orelse[0])

        test.outgoing.append(body)
        body.outgoing.append(test)

    def visit_Compare(self, node):
        vars = Vars()
        for i in node.comparators:
            vars.visit(i)
        vars.visit(node.left)

        label = LabelVisitor()
        label.visit(node)

        #CFG.append((label.result, vars.result))
        n = Node(label.result, variables = vars.result)
        CFG.append(n)
        return n

    def visit_Call(self, node):
        vars = Vars()
        label = LabelVisitor()

        vars.visit(node)
        label.visit(node)

        n = Node(label.result, variables = vars.result)
        CFG.append(n)
        return n


class Vars(ast.NodeVisitor):

    def visit_Name(self,node):
        self.result.append(node.id)

    def visit_Call(self,node):
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword)

    def visit_keyword(self, node):
        self.visit(node.value)

    def __init__(self):
        self.result = list()

class LabelVisitor(ast.NodeVisitor):
    def visit_Assign(self, node):
        for target in node.targets:
            self.visit(target)
        self.result = ' '.join((self.result,'='))
        self.visit(node.value)

    def visit_Compare(self,node):
        self.visit(node.left)
        for op,com in zip(node.ops,node.comparators):
            self.visit(op)
            self.visit(com)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.op)
        self.visit(node.right)

    #  operator = Add | Sub | Mult | MatMult | Div | Mod | Pow | LShift | RShift | BitOr | BitXor | BitAnd | FloorDiv
    def visit_Add(self, node):
        self.result = ' '.join((self.result, '+'))

    def visit_Sub(self, node):
        self.result = ' '.join((self.result, '-'))

    def visit_Mult(self, node):
        self.result = ' '.join((self.result, '*'))

    def vist_MatMult(self, node):
        self.result = ' '.join((self.result, 'x'))

    def visit_Div(self, node):
        self.result = ' '.join((self.result, '/'))

    def visit_Mod(self, node):
        self.result = ' '.join((self.result, '%'))

    def visit_Pow(self, node):
        self.result = ' '.join((self.result, '**'))

    def visit_LShift(self, node):
        self.result = ' '.join((self.result, '<<'))

    def visit_RShift(self, node):
        self.result = ' '.join((self.result, '>>'))

    def visit_BitOr(self, node):
        self.result = ' '.join((self.result, '|'))

    def visit_BitXor(self, node):
        self.result = ' '.join((self.result, '^'))

    def visit_BitAnd(self, node):
        self.result = ' '.join((self.result, '&'))

    def visit_FloorDiv(self, node):
        self.result = ' '.join((self.result, '//'))


    # cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
    def visit_Eq(self, node):
        self.result = ' '.join((self.result, '=='))

    def visit_Gt(self, node):
        self.result = ' '.join((self.result,'>'))

    def visit_Lt(self, node):
        self.result = ' '.join((self.result,'<'))

    def visit_NotEq(self,node):
        self.result = ' '.join((self.result,'!='))

    def visit_GtE(self,node):
        self.result = ' '.join((self.result,'>='))

    def visit_LtE(self,node):
        self.result = ' '.join((self.result,'<='))

    def visit_Is(self,node):
        self.result = ' '.join((self.result,'is'))

    def visit_IsNot(self,node):
        self.result = ' '.join((self.result,'is not'))

    def visit_In(self,node):
        self.result = ' '.join((self.result,'in'))

    def visit_NotIn(self,node):
        self.result = ' '.join((self.result,'not in'))

    def visit_Num(self, node):
        self.result = ' '.join((self.result, str(node.n)))
    def visit_Name(self,node):
        self.result = ' '.join((self.result, node.id))
    def visit_Str(self,node):
        self.result = ' '.join((self.result,node.s))
    def __init__(self):
        self.result = ''


Listener().visit(obj)

for n in CFG:
    print(n)
