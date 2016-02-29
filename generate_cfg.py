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
CFG_2 = list()

class Listener(ast.NodeVisitor):
    def visit_Assign(self, node):
        v = Vars()
        v.visit(node.value)
        
        CFG.append((node.targets[0].id, v.result))
       # CFG_2.append(Node(node._fields 
        self.generic_visit(node)
        

    def visit_Compare(self, node):
        v = Vars()
        for i in node.comparators:
            v.visit(i)
        
        CFG.append((node.left.id, type(node.ops[0]), v.result))
        self.generic_visit(node)

    def visit_Call(self, node):
        v = Vars()        
        if node.func.id == 'input':
            v.visit(node)
            CFG.append((v.result))
        elif node.func.id == 'print':
            CFG.append((node.func.id, node.args, node.keywords))

    def visit_Num(self, node):
        return node.n

class Vars(ast.NodeVisitor):
    
    def visit_Num(self,node):
        self.result.append(node.n)

    def visit_Name(self,node):
        self.result.append(node.id)

    def __init__(self):
        self.result = list()

    
    
Listener().visit(obj)

for n in CFG:
    print(n)
        
