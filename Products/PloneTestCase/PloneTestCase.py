#
# PloneTestCase
#

# $Id: PloneTestCase.py,v 1.11 2004/09/11 16:31:21 shh42 Exp $

from Testing import ZopeTestCase

from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import utils

from setup import portal_name
from setup import portal_owner
from setup import default_policy
from setup import default_products
from setup import default_user
from setup import setupPloneSite

from setup import _createHomeFolder
from setup import _takeOwnershipOfHomeFolder

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_base
from types import ListType


class PloneTestCase(ZopeTestCase.PortalTestCase):
    '''Base test case for Plone testing

       __implements__ = (IPortalTestCase, ISimpleSecurity, IExtensibleSecurity)

       See the ZopeTestCase docs for more
    '''

    def getPortal(self):
        '''Returns the portal object to the setup code.

           Do not call this method! Use the self.portal
           attribute to access the portal object from tests.
        '''
        return self.app[portal_name]

    def createMemberarea(self, member_id):
        '''Creates a minimal, no-nonsense memberarea.'''
        _createHomeFolder(self.portal, member_id)
        _takeOwnershipOfHomeFolder(self.portal, member_id)

    def setRoles(self, roles, name=default_user):
        '''Changes the user's roles. Assumes GRUF.'''
        self.assertEqual(type(roles), ListType)
        uf = self.portal.acl_users
        uf._updateUser(name, roles=roles)
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def getRoles(self, name=default_user):
        '''Returns the user's roles. Assumes GRUF.'''
        uf = self.portal.acl_users
        return uf.getUserById(name).getUserRoles()

    def setGroups(self, groups, name=default_user):
        '''Changes the user's groups. Assumes GRUF.'''
        self.assertEqual(type(groups), ListType)
        uf = self.portal.acl_users
        uf._updateUser(name, groups=groups)
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def getGroups(self, name=default_user):
        '''Returns the user's groups. Assumes GRUF.'''
        uf = self.portal.acl_users
        return uf.getUserById(name).getGroupsWithoutPrefix()

    def loginAsPortalOwner(self):
        '''Use this if you need to manipulate the portal itself.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)


class FunctionalTestCase(ZopeTestCase.Functional, PloneTestCase):
    '''Convenience class for functional unit testing'''

