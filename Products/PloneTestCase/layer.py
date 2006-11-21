#
# Layer support
#

# $Id$

import five
import setup


class ZCML:

    def setUp(cls):
        '''Sets up the CA by loading etc/site.zcml.'''
        five.safe_load_site()
    setUp = classmethod(setUp)

    def tearDown(cls):
        '''Cleans up the CA.'''
        five.cleanUp()
    tearDown = classmethod(tearDown)


class PloneSite(ZCML):

    def setUp(cls):
        '''Sets up the Plone site(s).'''
        setup.deferredSetup()
    setUp = classmethod(setUp)

    def tearDown(cls):
        '''Removes the Plone site(s).'''
        setup.cleanUp()
    tearDown = classmethod(tearDown)


# BBB
ZCMLLayer = ZCML

