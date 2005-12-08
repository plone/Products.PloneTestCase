import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

#import Products.PloneTestCase
from Testing.ZopeTestCase import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

from setup import PLACELESSSETUP, setUp, ITraversable, \
     tearDown, bootstrap_z3

PloneTestCase.setupPloneSite()

class TestFivePreLoaded(PloneTestCase.PloneTestCase):
    
    def afterSetUp(self):
        tearDown()
        PloneTestCase.installProduct('Five')

    def test_preloadedCA(self):
        assert ITraversable(SomeObject())
        tearDown()
        self.assertRaises(TypeError, ITraversable, self.folder)
        
class TestPlacelessSetup(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
        tearDown()
        
    def test_lifecycle(self):
        self.loginAsPortalOwner()
        # Setup according to Five's adapter test
        from zope.app.tests.placelesssetup import setUp, tearDown

        setUp()        

        import Products.Five.tests
        from Products.Five import zcml
        from Products.Five.tests.adapters import IAdapted, IDestination
        from Products.Five.tests.adapters import Adaptable, Origin    

        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('directives.zcml', Products.Five.tests)
        
        # Now we have a fixture that should work

        obj = Adaptable()
        adapted = IAdapted(obj)
        self.assertEqual(adapted.adaptedMethod(), 'Adapted: The method')

        # Now, lets test that the event tears this down
        tearDown()
        self.assertRaises(TypeError, IAdapted, obj)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    from placeless_test import TestPlacelessSetup
    suite.addTest(makeSuite(TestPlacelessSetup))
    suite.addTest(makeSuite(TestFivePreLoaded))
    return suite

if __name__ == '__main__':
    framework()
