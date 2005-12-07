from zope.interface import Interface, implements
from zope.app.tests.placelesssetup import tearDown

class ITearDownCA(Interface):
    """
    before the recreation of any fine placeless tests
    """
class TearDownCAEvent(object):
    implements(ITearDownCA)
    
def tearDownPlaceless(event):
    #print "whee %s" %event
    tearDown()

