#
# PloneTestCase
#

# $Id: PloneTestCase.py,v 1.17 2005/01/05 01:16:13 shh42 Exp $

from Testing import ZopeTestCase

from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import utils

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
from AccessControl.SecurityManagement import newSecurityManager


class PloneTestCase(ZopeTestCase.PortalTestCase):
    '''Base test case for Plone testing'''

    __implements__ = (IPloneSecurity,
                      ZopeTestCase.PortalTestCase.__implements__)

    def getPortal(self):
        '''Returns the portal object to the setup code.

           Do not call this method! Use the self.portal
           attribute to access the portal object from tests.
        '''
        return self.app[portal_name]

    def createMemberarea(self, member_id):
        '''Creates a minimal, no-nonsense memberarea.'''
        _createHomeFolder(self.portal, member_id)

    def setRoles(self, roles, name=default_user):
        '''Changes the user's roles. Assumes GRUF.'''
        uf = self.portal.acl_users
        uf._updateUser(name, roles=roles)
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def setGroups(self, groups, name=default_user):
        '''Changes the user's groups. Assumes GRUF.'''
        uf = self.portal.acl_users
        uf._updateUser(name, groups=groups)
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def loginAsPortalOwner(self):
        '''Use this when you need to manipulate the portal itself.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner)
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)


class FunctionalTestCase(ZopeTestCase.Functional, PloneTestCase):
    '''Base class for functional Plone tests'''

    __implements__ = (ZopeTestCase.Functional.__implements__,
                      PloneTestCase.__implements__)

