#
# Stop gap fix for abuse of ZTC.installProduct('Five')
#

# $Id$

import utils


class ZCMLLayer:

    def setUp(cls):
        utils.safe_load_site()
    setUp = classmethod(setUp)

    def tearDown(cls):
        utils.cleanUp()
    tearDown = classmethod(tearDown)

