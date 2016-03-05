from ast import parse
from ast import NodeVisitor
from label_visitor import LabelVisitor
from variable_visitor import VarsVisitor
from pprint import pprint

file_name = 'example.py'
#obj = compile(open(file_name).read(), file_name, 'exec', ast.PyCF_ONLY_AST)
obj = parse(open(file_name).read())


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

class Listener(NodeVisitor):
    def visit_Assign(self, node):
        label = LabelVisitor()
        label.visit(node)

        vars = VarsVisitor()
        vars.visit(node)

        n = Node(label.result,variables=vars.result)
        CFG.append(n)
        return n
        #CFG.append((label.result, vars.result))


    def visit_While(self, node):
        test = self.visit(node.test)
        #body_first = self.visit(node.body[0])
        body_last = self.visit(node.body[-1])
        if node.orelse:
            orelse = self.visit(node.orelse[0])


        print(type(body_last))
        #print('Outgoing: ' + str(body_first) + str(test))
#        test.outgoing.append(body_first)
        body_last.outgoing.append(test)
        #test.ingoing.append(node.body[-1])

    def visit_Compare(self, node):
        vars = VarsVisitor()
        for i in node.comparators:
            vars.visit(i)
        vars.visit(node.left)

        label = LabelVisitor()
        label.visit(node)

        #CFG.append((label.result, vars.result))
        print(vars.result)
        n = Node(label.result, variables = vars.result)
        CFG.append(n)
        return n


    #def visit(self,node):
        #print(node)
        #self.generic_visit(node)

    def visit_Call(self, node):
        vars = VarsVisitor()
        label = LabelVisitor()

        vars.visit(node)
        label.visit(node)

        n = Node(label.result, variables = vars.result)
        CFG.append(n)
        return n


Listener().visit(obj)

for n in CFG:
    print(n)
