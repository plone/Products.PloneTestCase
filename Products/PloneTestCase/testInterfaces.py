#
# Interface tests
#

# $Id: testInterfaces.py,v 1.1 2005/01/02 19:28:40 shh42 Exp $

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.interfaces import *

from Interface.Verify import verifyObject


class TestPloneTestCase(PloneTestCase.PloneTestCase):

    _configure_portal = 0

    def getPortal(self):
        return None

    def testIProfiled(self):
        self.failUnless(verifyObject(IProfiled, self))

    def testIPortalTestCase(self):
        self.failUnless(verifyObject(IPortalTestCase, self))

    def testIPloneSecurity(self):
        self.failUnless(verifyObject(IPloneSecurity, self))


class TestFunctionalTestCase(PloneTestCase.FunctionalTestCase):

    _configure_portal = 0

    def getPortal(self):
        return None

    def testIFunctional(self):
        self.failUnless(verifyObject(IFunctional, self))

    def testIProfiled(self):
        self.failUnless(verifyObject(IProfiled, self))

    def testIPortalTestCase(self):
        self.failUnless(verifyObject(IPortalTestCase, self))

    def testIPloneSecurity(self):
        self.failUnless(verifyObject(IPloneSecurity, self))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneTestCase))
    suite.addTest(makeSuite(TestFunctionalTestCase))
    return suite

if __name__ == '__main__':
    framework()

