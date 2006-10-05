#
# Stop gap fix for abuse of ZTC.installProduct('Five')
#

# $Id$

from Testing.ZopeTestCase.utils import *

try:
    from zope.testing.cleanup import cleanUp
except ImportError:
    try:
        from Testing.ZopeTestCase.placeless import tearDown as cleanUp
    except ImportError:
        # Zope <= 2.7
        def cleanUp(): pass


def cleanUp():
    """Clean up component architecture"""
    cleanUp()
    import Products.Five.zcml as zcml
    zcml._initialized = 0


def setDebugMode(mode):
    """
    Allows manual setting of Five's inspection of debug mode to allow for
    zcml to fail meaningfully
    """
    import Products.Five.fiveconfigure as fc
    fc.debug_mode = mode


def safe_load_site():
    """Load entire component architecture (w/ debug mode on)"""
    cleanUp()
    setDebugMode(1)
    import Products.Five.zcml as zcml
    zcml.load_site()
    setDebugMode(0)


def safe_load_site_wrapper(function):
    """Wrap function with a temporary loading of entire component architecture"""
    def wrapper(*args, **kw):
        safe_load_site()
        value = function(*args, **kw)
        cleanUp()
        return value
    return wrapper

