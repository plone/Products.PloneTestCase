#
# PloneTestCase setup
#

# $Id$

from Testing import ZopeTestCase
from Testing.ZopeTestCase import placeless

ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('CMFCalendar')
ZopeTestCase.installProduct('CMFTopic')
ZopeTestCase.installProduct('DCWorkflow')
ZopeTestCase.installProduct('CMFUid', quiet=1)
ZopeTestCase.installProduct('CMFActionIcons')
ZopeTestCase.installProduct('CMFQuickInstallerTool')
ZopeTestCase.installProduct('CMFFormController')

# Check for Plone 2.5 or above
try:
    from Products.CMFPlone.tests.utils import setupBrowserIdManager
except ImportError:
    PLONE25 = 0
else:
    PLONE25=1
    ZopeTestCase.installProduct('CMFPlacefulWorkflow')
    # Quiet for now as PlonePAS isn't merged
    ZopeTestCase.installProduct('PluggableAuthService', quiet=1)
    ZopeTestCase.installProduct('PluginRegistry', quiet=1)
    ZopeTestCase.installProduct('PasswordResetTool', quiet=1)
    ZopeTestCase.installProduct('PlonePAS', quiet=1)

try:
    import Products.Five 
    PLACELESS = True
except ImportError:
    PLACELESS = False
    
# Check for Plone 2.1 or above
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    PLONE21 = 0
    ZopeTestCase.installProduct('GroupUserFolder')
    ZopeTestCase.installProduct('ZCTextIndex')
    ZopeTestCase.installProduct('CMFPlone')
else:
    PLONE21 = 1
    ZopeTestCase.installProduct('ResourceRegistries')
    ZopeTestCase.installProduct('GroupUserFolder')
    ZopeTestCase.installProduct('ZCTextIndex')
    ZopeTestCase.installProduct('ExtendedPathIndex')
    ZopeTestCase.installProduct('SecureMailHost')
    ZopeTestCase.installProduct('CMFPlone')
    ZopeTestCase.installProduct('Archetypes')
    ZopeTestCase.installProduct('MimetypesRegistry', quiet=1)
    ZopeTestCase.installProduct('PortalTransforms', quiet=1)
    ZopeTestCase.installProduct('ATContentTypes')
    ZopeTestCase.installProduct('ATReferenceBrowserWidget')

ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('PageTemplates', quiet=1)
ZopeTestCase.installProduct('PythonScripts', quiet=1)
ZopeTestCase.installProduct('ExternalMethod', quiet=1)

from Testing.ZopeTestCase import transaction
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl import getSecurityManager
from Acquisition import aq_base
from time import time

if PLONE21:
    from Products.CMFPlone.utils import _createObjectByType
else:
    from Products.CMFPlone.PloneUtilities import _createObjectByType

portal_name = 'plone'
portal_owner = 'portal_owner'
default_policy = 'Default Plone'
default_products = ()
default_user = ZopeTestCase.user_name
default_password = ZopeTestCase.user_password

#@placeless.temporaryPlacelessSetup(placeless_available=PLACELESS)
def setupPloneSite(id=portal_name, policy=default_policy, products=default_products,
                   quiet=0, with_default_memberarea=1):
    '''Creates a Plone site and/or quickinstalls products into it.'''
    PortalSetup(id, policy, products, quiet, with_default_memberarea).run()

setupPloneSite = placeless.temporaryPlacelessSetup(setupPloneSite, placeless_available=PLACELESS)

class PortalSetup(object):
    '''Creates a Plone site and/or quickinstalls products into it.'''

    def __init__(self, id, policy, products, quiet, with_default_memberarea):
        self.id = id
        self.policy = policy
        self.products = products
        self.quiet = quiet
        self.with_default_memberarea = with_default_memberarea

    def run(self):
        self.app = self._app()
        try:
            uf = self.app.acl_users
            if uf.getUserById(portal_owner) is None:
                # Add portal owner
                uf.userFolderAddUser(portal_owner, default_password, ['Manager'], [])
            if not hasattr(aq_base(self.app), self.id):
                # Log in and create site
                self._login(uf, portal_owner)
                self._optimize()
                self._setupPloneSite()
            if hasattr(aq_base(self.app), self.id):
                # Log in as portal owner
                self._login(uf, portal_owner)
                self._setupProducts()
        finally:
            self._abort()
            self._close()
            self._logout()

    def _setupPloneSite(self):
        '''Creates the Plone site.'''
        start = time()
        if self.policy == default_policy:
            self._print('Adding Plone Site ... ')
        else:
            self._print('Adding Plone Site (%s) ... ' % self.policy)
        # Add Plone site
        factory = self.app.manage_addProduct['CMFPlone']
        factory.manage_addSite(self.id, create_userfolder=1, custom_policy=self.policy)
        # Precreate default memberarea to speed up the tests
        if self.with_default_memberarea:
            self._setupHomeFolder()
        # Setup a browser id manager for the 2.5 status messages
        if PLONE25:
            setupBrowserIdManager(self.app)
        self._commit()
        self._print('done (%.3fs)\n' % (time()-start,))

    def _setupProducts(self):
        '''Quickinstalls products into the Plone site.'''
        qi = self.app[self.id].portal_quickinstaller
        for product in self.products:
            if not qi.isProductInstalled(product):
                if qi.isProductInstallable(product):
                    start = time()
                    self._print('Adding %s ... ' % (product,))
                    qi.installProduct(product)
                    self._commit()
                    self._print('done (%.3fs)\n' % (time()-start,))
                else:
                    self._print('Adding %s ... NOT INSTALLABLE\n' % (product,))

    def _setupHomeFolder(self):
        '''Creates the default user's memberarea.'''
        _createHomeFolder(self.app[self.id], default_user, 0)

    def _optimize(self):
        '''Applies optimizations to the PloneGenerator.'''
        _optimize()

    def _app(self):
        '''Opens a ZODB connection and returns the app object.'''
        return ZopeTestCase.app()

    def _close(self):
        '''Closes the ZODB connection.'''
        ZopeTestCase.close(self.app)

    def _login(self, uf, name):
        '''Logs in as user 'name' from user folder 'uf'.'''
        user = uf.getUserById(name).__of__(uf)
        newSecurityManager(None, user)

    def _logout(self):
        '''Logs out.'''
        noSecurityManager()

    def _commit(self):
        '''Commits the transaction.'''
        transaction.commit()

    def _abort(self):
        '''Aborts the transaction.'''
        transaction.abort()

    def _print(self, msg):
        '''Prints msg to stderr.'''
        if not self.quiet:
            ZopeTestCase._print(msg)


def _createHomeFolder(portal, member_id, take_ownership=1):
    '''Creates a memberarea if it does not already exist.'''
    pm = portal.portal_membership
    members = pm.getMembersFolder()

    if not hasattr(aq_base(members), member_id):
        # Create home folder
        _createObjectByType('Folder', members, id=member_id)
        # Create personal folder
        home = pm.getHomeFolder(member_id)
        _createObjectByType('Folder', home, id=pm.personal_id)
        # Uncatalog personal folder
        personal = pm.getPersonalFolder(member_id)
        personal.unindexObject()

    if take_ownership:
        user = portal.acl_users.getUserById(member_id)
        if user is None:
            raise ValueError, 'Member %s does not exist' % member_id
        if not hasattr(user, 'aq_base'):
            user = user.__of__(portal.acl_users)
        # Take ownership of home folder
        home = pm.getHomeFolder(member_id)
        home.changeOwnership(user)
        home.__ac_local_roles__ = None
        home.manage_setLocalRoles(member_id, ['Owner'])
        # Take ownership of personal folder
        personal = pm.getPersonalFolder(member_id)
        personal.changeOwnership(user)
        personal.__ac_local_roles__ = None
        personal.manage_setLocalRoles(member_id, ['Owner'])


def _optimize():
    '''Significantly reduces portal creation time.'''
    # Don't compile expressions on creation
    def __init__(self, text):
        self.text = text
    from Products.CMFCore.Expression import Expression
    Expression.__init__ = __init__
    # Don't clone actions but convert to list only
    def _cloneActions(self):
        return list(self._actions)
    from Products.CMFCore.ActionProviderBase import ActionProviderBase
    ActionProviderBase._cloneActions = _cloneActions
    # Don't setup default directory views
    def setupDefaultSkins(self, p):
        from Products.CMFCore.utils import getToolByName
        ps = getToolByName(p, 'portal_skins')
        ps.manage_addFolder(id='custom')
        ps.addSkinSelection('Basic', 'custom')
    from Products.CMFPlone.Portal import PloneGenerator
    PloneGenerator.setupDefaultSkins = setupDefaultSkins
    # Don't setup default Members folder
    def setupMembersFolder(self, p):
        pass
    PloneGenerator.setupMembersFolder = setupMembersFolder
    # Don't setup Plone content (besides Members folder)
    def setupPortalContent(self, p):
        _createObjectByType('Large Plone Folder', p, id='Members', title='Members')
        if not PLONE21: p.Members.unindexObject()
    PloneGenerator.setupPortalContent = setupPortalContent
    # Don't populate type fields in the ConstrainTypesMixin schema
    if PLONE21:
        def _ct_defaultAddableTypeIds(self):
            return []
        from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixin
        ConstrainTypesMixin._ct_defaultAddableTypeIds = _ct_defaultAddableTypeIds

