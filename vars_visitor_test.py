import unittest
from vars_visitor import VarsVisitor
from ast import parse

class LabelVisitorTestCase(unittest.TestCase):
    '''Baseclass for LabelVisitor tests'''

    def perform_vars_on_expression(self, expr):
        obj = parse(expr)
        vars = VarsVisitor()
        vars.visit(obj)

        return vars

class LabelVisitorTest(LabelVisitorTestCase):
    def test_assign_var_and_num(self):
        vars = self.perform_vars_on_expression('a = 1')
        self.assertEqual(vars.result,['a'])

    def test_assign_var_and_var(self):
        vars = self.perform_vars_on_expression('a = x')
        self.assertEqual(vars.result,['a','x'])
