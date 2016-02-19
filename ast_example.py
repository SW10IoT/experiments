from parser import expr
from parser import suite
from parser import st2list
import symbol
import token
from pprint import pprint

m = dict(token.tok_name.items())
m.update(symbol.sym_name.items())

print('Integer mapped to their token or symbol:')
print(sorted(m.items(), key = lambda p: p[0]))
print()

def shallow(ast):
    if not isinstance(ast, list): return ast
    if len(ast) == 2: return shallow(ast[1])
    return [m[ast[0]]] + [shallow(a) for a in ast[1:]]

st = suite(open('ast_example.py', 'r').read())
stl = st2list(st)
print('AST with integers:')
pprint(stl)
print()
ast = shallow(stl)
print('AST with integers mapped to tokens and symbols:')
pprint(ast)

