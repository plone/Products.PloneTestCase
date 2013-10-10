#
# Interface tests
#

import os
import sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase import setup
from Products.PloneTestCase.interfaces import *

if setup.Z3INTERFACES:
    from zope.interface.verify import verifyClass
    from zope.interface.verify import verifyObject
else:
    from Interface.Verify import verifyClass
    from Interface.Verify import verifyObject


class TestPloneTestCase(PloneTestCase.PloneTestCase):

    _configure_portal = 0

    def _portal(self):
        return None

    def testIPortalTestCase(self):
        self.assertTrue(verifyClass(IPortalTestCase,
                                    PloneTestCase.PloneTestCase))
        self.assertTrue(verifyObject(IPortalTestCase, self))

    def testIPloneTestCase(self):
        self.assertTrue(verifyClass(IPloneTestCase,
                                    PloneTestCase.PloneTestCase))
        self.assertTrue(verifyObject(IPloneTestCase, self))

    def testIPloneSecurity(self):
        self.assertTrue(verifyClass(IPloneSecurity,
                                    PloneTestCase.PloneTestCase))
        self.assertTrue(verifyObject(IPloneSecurity, self))


class TestFunctionalTestCase(PloneTestCase.FunctionalTestCase):

    _configure_portal = 0

    def _portal(self):
        return None

    def testIFunctional(self):
        self.assertTrue(verifyClass(IFunctional,
                                    PloneTestCase.FunctionalTestCase))
        self.assertTrue(verifyObject(IFunctional, self))

    def testIPortalTestCase(self):
        self.assertTrue(verifyClass(IPortalTestCase,
                                    PloneTestCase.FunctionalTestCase))
        self.assertTrue(verifyObject(IPortalTestCase, self))

    def testIPloneTestCase(self):
        self.assertTrue(verifyClass(IPloneTestCase,
                                    PloneTestCase.FunctionalTestCase))
        self.assertTrue(verifyObject(IPloneTestCase, self))

    def testIPloneSecurity(self):
        self.assertTrue(verifyClass(IPloneSecurity,
                                    PloneTestCase.FunctionalTestCase))
        self.assertTrue(verifyObject(IPloneSecurity, self))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneTestCase))
    suite.addTest(makeSuite(TestFunctionalTestCase))
    return suite

if __name__ == '__main__':
    framework()
