import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

#import Products.PloneTestCase
from Testing.ZopeTestCase import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

from Testing.ZopeTestCase.placeless import tearDown, setUp
from zope.app.traversing.interfaces import ITraversable

PloneTestCase.setupPloneSite()
        
class TestPlacelessSetup(PloneTestCase.PloneTestCase):
        
    def test_lifecycle(self):
        self.loginAsPortalOwner()
        # Setup according to Five's adapter test

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
    suite.addTest(makeSuite(TestPlacelessSetup))
    return suite

if __name__ == '__main__':
    framework()
