#
# PloneTestCase interfaces
#

# $Id: interfaces.py,v 1.2 2005/02/25 11:02:43 shh42 Exp $

from Testing.ZopeTestCase.interfaces import *


class IPloneSecurity(IPortalSecurity):

    def setGroups(groups, name=None):
        '''Changes the groups assigned to a user.
           If the 'name' argument is omitted, changes the
           groups of the default user.
        '''

    def loginAsPortalOwner():
        '''Logs in as the user owning the portal object.
           Use this when you need to manipulate the portal
           itself.
        '''

    def addProduct(name):
        '''Quickinstalls a product into the Plone site.
           This is alternative to passing a 'products'
           argument to setupPloneSite.
        '''

