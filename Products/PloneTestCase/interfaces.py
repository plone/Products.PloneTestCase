#
# PloneTestCase interfaces
#

# $Id: interfaces.py,v 1.1 2005/01/02 19:28:40 shh42 Exp $

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

