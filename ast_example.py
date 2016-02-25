from parser import expr
from parser import suite
from parser import st2list
import symbol
import token
from pprint import pprint

def get_token_symbol_map():
    m = dict(token.tok_name.items())
    m.update(symbol.sym_name.items())
    return m

TOKEN_SYMBOL_MAP = get_token_symbol_map()

def shallow(ast):
    if not isinstance(ast, list): return ast
    if len(ast) == 2: return shallow(ast[1])
    return [TOKEN_SYMBOL_MAP[ast[0]]] + [shallow(a) for a in ast[1:]]

def file_to_ast(file_path, raw=False, line_number=False):
    m = get_token_symbol_map()
    st_object = suite(open(file_path, 'r').read())
    raw_ast = st2list(st_object, line_info=line_number)
    if raw:
        return raw_ast
    return shallow(raw_ast)

def ast_example():
    print('Integer mapped to their token or symbol:')
    print(sorted(TOKEN_SYMBOL_MAP.items(), key = lambda p: p[0]))
    print()
    print('Raw AST:')
    pprint(file_to_ast('ast_example.py', raw=True))
    print()
    print('AST with integers mapped to tokens and symbols:')
    pprint(file_to_ast('ast_example.py'))
