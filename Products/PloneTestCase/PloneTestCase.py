#
# PloneTestCase
#

from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import installProduct

try:
    from Testing.ZopeTestCase import hasPackage
    from Testing.ZopeTestCase import installPackage
except ImportError:
    pass

from Testing.ZopeTestCase import Sandboxed
from Testing.ZopeTestCase import Functional
from Testing.ZopeTestCase import PortalTestCase

from version import PLONE21
from version import PLONE25
from version import PLONE30
from version import PLONE31
from version import PLONE32
from version import PLONE33
from version import PLONE40
from version import PLONE50
from setup import USELAYER
from setup import Z3INTERFACES
from setup import portal_name
from setup import portal_owner
from setup import default_policy
from setup import default_products
from setup import default_base_profile
from setup import default_extension_profiles
from setup import default_user
from setup import default_password
from setup import _placefulSetUp
from setup import _placefulTearDown
from setup import _createHomeFolder

from setup import setupPloneSite

from interfaces import IPloneTestCase
from interfaces import IPloneSecurity

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from warnings import warn

import utils
import setup


class PloneTestCase(PortalTestCase):
    '''Base test case for Plone testing'''

    if Z3INTERFACES:
        from zope.interface import implements
        implements(IPloneTestCase, IPloneSecurity)
    else:
        __implements__ = (IPloneTestCase, IPloneSecurity,
                          PortalTestCase.__implements__)

    if USELAYER:
        import layer
        layer = layer.PloneSite

    def _portal(self):
        '''Returns the portal object for a test.'''
        portal = self.getPortal()
        if PLONE30:
            _placefulSetUp(portal)
        return portal

    def _setup(self):
        '''Configures the portal.'''
        PortalTestCase._setup(self)
        if PLONE30 and self.portal is not None:
            self._refreshSkinData()

    def _clear(self, call_close_hook=0):
        '''Clears the fixture.'''
        if PLONE30:
            self._resetRAMCache()
        PortalTestCase._clear(self, call_close_hook)
        if PLONE30:
            _placefulTearDown()

    def _resetRAMCache(self):
        '''Resets memoize RAMCaches.'''
        from plone.memoize.ram import global_cache
        global_cache.invalidateAll()
        from zope.component import queryUtility
        from plone.memoize.ram import IRAMCache
        cache = queryUtility(IRAMCache)
        if cache is not None:
            cache.invalidateAll()

    # Portal interface

    def getPortal(self):
        '''Returns the portal object.

           Do not call this method! Use the self.portal
           attribute to access the portal object from tests.
        '''
        return getattr(self.app, portal_name)

    def createMemberarea(self, name):
        '''Creates a minimal memberarea.'''
        _createHomeFolder(self.portal, name)

    # Security interface

    def setRoles(self, roles, name=default_user):
        '''Changes the user's roles.'''
        uf = self.portal.acl_users
        if PLONE25:
            uf.userFolderEditUser(name, None, utils.makelist(roles), [])
        else:
            uf._updateUser(name, roles=utils.makelist(roles))
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def setGroups(self, groups, name=default_user):
        '''Changes the user's groups.'''
        uf = self.portal.acl_users
        if PLONE25:
            uf.userSetGroups(name, utils.makelist(groups))
        else:
            uf._updateUser(name, groups=utils.makelist(groups))
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def loginAsPortalOwner(self):
        '''Use if - AND ONLY IF - you need to manipulate
           the portal object itself.
        '''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner)
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)

    # Plone interface

    def addProfile(self, name):
        '''Imports an extension profile into the site.'''
        sm = getSecurityManager()
        self.loginAsPortalOwner()
        try:
            installed = getattr(self.portal, '_installed_profiles', {})
            if not installed.has_key(name):
                setup = self.portal.portal_setup
                profile_id = 'profile-%s' % (name,)
                if PLONE30:
                    setup.runAllImportStepsFromProfile(profile_id)
                else:
                    saved = setup.getImportContextID()
                    try:
                        setup.setImportContext(profile_id)
                        setup.runAllImportSteps()
                    finally:
                        setup.setImportContext(saved)
                self._refreshSkinData()
        finally:
            setSecurityManager(sm)

    def addProduct(self, name):
        '''Quickinstalls a product into the site.'''
        sm = getSecurityManager()
        self.loginAsPortalOwner()
        try:
            qi = self.portal.portal_quickinstaller
            if not qi.isProductInstalled(name):
                qi.installProduct(name)
                self._refreshSkinData()
        finally:
            setSecurityManager(sm)


class FunctionalTestCase(Functional, PloneTestCase):
    '''Base class for functional Plone tests'''

    if not Z3INTERFACES:
        __implements__ = (Functional.__implements__,
                          PloneTestCase.__implements__)

