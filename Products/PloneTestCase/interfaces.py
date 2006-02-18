#
# PloneTestCase interfaces
#

# $Id$

from Testing.ZopeTestCase import interfaces

class IPloneSecurity(interfaces.IPortalSecurity):

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


class IPloneTestCase(interfaces.IPortalTestCase):

    def addProduct(name):
        '''Quickinstalls a product into the Plone site.
           This is an alternative to passing a 'products'
           argument to 'setupPloneSite'.
        '''

