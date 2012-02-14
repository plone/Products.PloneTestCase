#
# Component architecture support
#

from __future__ import nested_scopes

try:
    from zope.testing.cleanup import cleanUp as _cleanUp
except ImportError:
    try:
        from zope.app.testing.placelesssetup import tearDown as _cleanUp
    except ImportError:
        # Zope < 2.8
        def _cleanUp(): pass


def cleanUp():
    '''Cleans up the component architecture.'''
    _cleanUp()
    try:
        from Zope2.App import zcml
        zcml._initialized = 0
    except ImportError:
        pass
    try:
        from Products.Five import zcml
        zcml._initialized = 0
    except ImportError:
        pass


def setDebugMode(mode):
    '''Allows manual setting of Five's inspection of debug mode
       to allow for ZCML to fail meaningfully.
    '''
    try:
        from OFS import metaconfigure
    except ImportError:
        from Products.Five import fiveconfigure as metaconfigure
    metaconfigure.debug_mode = mode


def safe_load_site():
    '''Loads entire component architecture (w/ debug mode on).'''
    cleanUp()
    setDebugMode(1)
    try:
        from Zope2.App import zcml
    except ImportError:
        from Products.Five import zcml
    zcml.load_site()
    try:
        from Zope2.App.schema import configure_vocabulary_registry
    except ImportError:
        try:
            from zope.schema.vocabulary import setVocabularyRegistry
            from Products.Five.schema import Zope2VocabularyRegistry
        except ImportError:
            pass
        else:
            setVocabularyRegistry(Zope2VocabularyRegistry())
    else:
        configure_vocabulary_registry()
    setDebugMode(0)


def safe_load_site_wrapper(func):
    '''Wraps func with a temporary loading of entire component
       architecture. Used as a decorator.
    '''
    def wrapped_func(*args, **kw):
        safe_load_site()
        value = func(*args, **kw)
        cleanUp()
        return value
    return wrapped_func

