import ast
from pprint import pprint
file_name = 'example.py'

#obj = compile(open(file_name).read(), file_name, 'exec', ast.PyCF_ONLY_AST)
obj = ast.parse(open(file_name).read())


class Node:
    '''CFG Node'''
    
    def __init__(self, outgoing, ingoing=None, variables=None):
        self.ingoing = ingoing
        self.outgoing = outgoing
        self.variables = variables


CFG = list()


class Listener(ast.NodeVisitor):
    def visit_Assign(self, node):
        label = LabelVisitor()
        label.visit(node)
        
        vars = Vars()
        vars.visit(node)
        
        CFG.append((label.result, vars.result))

    def visit_Compare(self, node):
        vars = Vars()
        for i in node.comparators:
            vars.visit(i)
        vars.visit(node.left)

        label = LabelVisitor()
        label.visit(node)
        
        CFG.append((label.result, vars.result))

    def visit_Call(self, node):
        v = Vars()        
        if node.func.id == 'input':
            v.visit(node)
            CFG.append((v.result))
        elif node.func.id == 'print':
            v.visit(node)
            CFG.append((node.func.id, node.args, node.keywords))

    def visit_Num(self, node):
        return node.n

class Vars(ast.NodeVisitor):
    
    def visit_Name(self,node):
        self.result.append(node.id)

    def visit_Call(self,node):
        self.result.append((node.args,node.keywords))
    
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
        
