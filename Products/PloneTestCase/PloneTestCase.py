#
# PloneTestCase
#

# $Id$

from Testing.ZopeTestCase import PortalTestCase
from Testing.ZopeTestCase import Functional

from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase import utils

from setup import PLONE21
from setup import portal_name
from setup import portal_owner
from setup import default_policy
from setup import default_products
from setup import default_user
from setup import default_password
from setup import setupPloneSite
from setup import _createHomeFolder

from interfaces import IPloneSecurity
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager


class PloneTestCase(PortalTestCase):
    '''Base test case for Plone testing'''

    __implements__ = (IPloneSecurity,
                      PortalTestCase.__implements__)

    def getPortal(self):
        '''Returns the portal object to the setup code.

           DO NOT CALL THIS METHOD! Use the self.portal
           attribute to access the portal object from tests.
        '''
        return self.app[portal_name]

    def createMemberarea(self, name):
        '''Creates a minimal, no-nonsense memberarea.'''
        _createHomeFolder(self.portal, name)

    def setRoles(self, roles, name=default_user):
        '''Changes the user's roles. Assumes GRUF.'''
        uf = self.portal.acl_users
        uf._updateUser(name, roles=utils.makelist(roles))
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def setGroups(self, groups, name=default_user):
        '''Changes the user's groups. Assumes GRUF.'''
        uf = self.portal.acl_users
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

    __implements__ = (Functional.__implements__,
                      PloneTestCase.__implements__)

