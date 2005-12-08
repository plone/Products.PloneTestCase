import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

#import Products.PloneTestCase
from Testing.ZopeTestCase import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

PloneTestCase.setupPloneSite()
PloneTestCase.installProduct('Five')

class TestFivePreLoaded(PloneTestCase.PloneTestCase):

    def test_ca_notloaded(self):
        self.assertRaises(TypeError, ITraversable, self.folder)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    from placeless_test import TestPlacelessSetup
    suite.addTest(makeSuite(TestFivePreLoaded))
    return suite

if __name__ == '__main__':
    framework()
