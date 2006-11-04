#
# PloneTestCase
#

# $Id$

from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import installProduct

from Testing.ZopeTestCase import Sandboxed
from Testing.ZopeTestCase import Functional
from Testing.ZopeTestCase import PortalTestCase

from setup import PLONE21
from setup import PLONE25
from setup import PLONE30
from setup import portal_name
from setup import portal_owner
from setup import default_policy
from setup import default_products
from setup import default_base_profile
from setup import default_extension_profiles
from setup import default_user
from setup import default_password
from setup import setupPloneSite
from setup import _createHomeFolder

from interfaces import IPloneTestCase
from interfaces import IPloneSecurity

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from warnings import warn

import setup
import utils


class PloneTestCase(PortalTestCase):
    '''Base test case for Plone testing'''

    if setup.Z3INTERFACES:
        from zope.interface import implements
        implements(IPloneTestCase, IPloneSecurity)
    else:
        __implements__ = (IPloneTestCase, IPloneSecurity,
                          PortalTestCase.__implements__)

    if setup.USELAYER:
        import layer
        layer = layer.ZCMLLayer

    # TODO: This is a bit of an ugly hack, but I couldn't spot a nicer place 
    # to put it. Making this change in PortalSetup doesn't work though.
    if PLONE30:
        def _setup(self):
            PortalTestCase._setup(self)
            # Set the local component registry
            from zope.app.component.hooks import setSite, setHooks
            setHooks()
            setSite(self.portal)

    def _portal(self):
        '''Returns the portal object for a test.'''
        try:
            return self.getPortal(1)
        except TypeError:
            return self.getPortal()

    def getPortal(self, called_by_framework=0):
        '''Returns the portal object to the setup code.

           DO NOT CALL THIS METHOD! Use the self.portal
           attribute to access the portal object from tests.
        '''
        if not called_by_framework:
            warn('Calling getPortal is not allowed, please use the '
                 'self.portal attribute.', UserWarning, 2)
        return getattr(self.app, portal_name)

    def createMemberarea(self, name):
        '''Creates a minimal, no-nonsense memberarea.'''
        _createHomeFolder(self.portal, name)

    def setRoles(self, roles, name=default_user):
        """Changes the user's roles. Assumes GRUF."""
        uf = self.portal.acl_users
        # Plone 2.5 uses PlonePAS instead of GRUF
        if PLONE25:
            uf.userFolderEditUser(name, None, utils.makelist(roles), [])
        else:
            uf._updateUser(name, roles=utils.makelist(roles))
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def setGroups(self, groups, name=default_user):
        """Changes the user's groups. Assumes GRUF."""
        uf = self.portal.acl_users
        # Plone 2.5 uses PlonePAS instead of GRUF
        if PLONE25:
            uf.userSetGroups(name, utils.makelist(groups))
        else:
            uf._updateUser(name, groups=utils.makelist(groups))
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def loginAsPortalOwner(self):
        """Use if - AND ONLY IF - you need to manipulate
           the portal object itself.
        """
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner)
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)

    def addProduct(self, name):
        '''Quickinstalls a product into the Plone site.'''
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

    if not setup.Z3INTERFACES:
        __implements__ = (Functional.__implements__,
                          PloneTestCase.__implements__)

