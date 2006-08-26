import unittest
import os, sys

import os, sys

suite = unittest.TestSuite()

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py')) 

names = os.listdir(os.path.dirname(__file__))
tests = [x[:-3] for x in names \
         if x.startswith('test') and x.endswith('.py') \
         and not x == 'tests.py']

import Products.PloneTestCase
for test in tests:
    m = __import__("Products.PloneTestCase.%s" %test)
    m = getattr(Products.PloneTestCase, test)
    if hasattr(m, 'test_suite'):
        suite.addTest(m.test_suite())

def test_suite():
    return suite
