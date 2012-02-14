#
# Allow testrunners to pick up tests
#

import unittest
import os
import Products.PloneTestCase

suite = unittest.TestSuite()

try:
    names = os.listdir(os.path.dirname(__file__))
except OSError:
    tests = []
else:
    tests = [x[:-3] for x in names
             if x.startswith('test') and x.endswith('.py')
             and x != 'tests.py']

for test in tests:
    m = __import__('Products.PloneTestCase.%s' % test)
    m = getattr(Products.PloneTestCase, test)
    if hasattr(m, 'test_suite'):
        suite.addTest(m.test_suite())

def test_suite():
    return suite

