#
# Stop gap fix for abuse of ZTC.installProduct('Five')
#

# $Id$

import utils


class ZCMLLayer:

    def setUp(cls):
        '''Sets up the CA by loading etc/site.zcml.'''
        utils.safe_load_site()
    setUp = classmethod(setUp)

    def tearDown(cls):
        '''Cleans up the CA.'''
        utils.cleanUp()
    tearDown = classmethod(tearDown)

