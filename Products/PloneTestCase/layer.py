"""Stop gap fix for abuse of ZTC.installProduct('Five') """

import utils
class ZCMLLayer:

    def setUp(cls):
        # this keeps five from hiding config errors while toggle debug
        # back on to let PTC perform efficiently
        utils.safe_load_site()
    setUp=classmethod(setUp)

    def tearDown(cls):
        utils.cleanUp()
    tearDown=classmethod(tearDown)
