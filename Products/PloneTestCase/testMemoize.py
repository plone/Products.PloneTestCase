#
# Test memoize RAMCache cleanup
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
PloneTestCase.setupPloneSite()


class TestMemoize(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.called = []
        self.func = self._makeOne()

    def _makeOne(self):
        from plone.memoize.ram import cache
        def mykey(func, a, b):
            return (a, b) # Deliberately stupid cache key
        @cache(mykey)
        def foo(a, b):
            self.called.append((a, b))
            return a+b
        return foo

    def testMemoize_1(self):
        self.assertEqual(self.func(1, 2), 3)
        self.assertEqual(self.called, [(1, 2)])
        # Next time the value is cached and the func
        # is not called
        self.called = []
        self.assertEqual(self.func(1, 2), 3)
        self.assertEqual(self.called, [])

    def testMemoize_2(self):
        # The cache has been reset between tests
        self.assertEqual(self.func(1, 2), 3)
        self.assertEqual(self.called, [(1, 2)])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMemoize))
    return suite

if __name__ == '__main__':
    framework()

