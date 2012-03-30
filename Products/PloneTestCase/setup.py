#
# PloneTestCase setup
#

from Testing import ZopeTestCase

from version import PLONE21
from version import PLONE25
from version import PLONE30
from version import PLONE31
from version import PLONE32
from version import PLONE33
from version import PLONE40
from version import PLONE42
from version import PLONE50

def install_products():
    ZopeTestCase.installProduct('CMFCore', quiet=1)
    ZopeTestCase.installProduct('CMFDefault', quiet=1)
    ZopeTestCase.installProduct('CMFCalendar', quiet=1)
    ZopeTestCase.installProduct('CMFTopic', quiet=1)
    ZopeTestCase.installProduct('DCWorkflow', quiet=1)
    ZopeTestCase.installProduct('CMFUid', quiet=1)
    ZopeTestCase.installProduct('CMFActionIcons', quiet=1)
    ZopeTestCase.installProduct('CMFQuickInstallerTool', quiet=1)
    ZopeTestCase.installProduct('CMFFormController', quiet=1)
    ZopeTestCase.installProduct('GroupUserFolder', quiet=1)
    ZopeTestCase.installProduct('ZCTextIndex', quiet=1)
    ZopeTestCase.installProduct('CMFPlone', quiet=1)

    if PLONE21:
        ZopeTestCase.installProduct('Archetypes', quiet=1)
        ZopeTestCase.installProduct('MimetypesRegistry', quiet=1)
        ZopeTestCase.installProduct('PortalTransforms', quiet=1)
        ZopeTestCase.installProduct('ATContentTypes', quiet=1)
        ZopeTestCase.installProduct('ATReferenceBrowserWidget', quiet=1)
        ZopeTestCase.installProduct('CMFDynamicViewFTI', quiet=1)
        ZopeTestCase.installProduct('ExternalEditor', quiet=1)
        ZopeTestCase.installProduct('ExtendedPathIndex', quiet=1)
        ZopeTestCase.installProduct('ResourceRegistries', quiet=1)
        ZopeTestCase.installProduct('SecureMailHost', quiet=1)

    if PLONE25:
        ZopeTestCase.installProduct('CMFPlacefulWorkflow', quiet=1)
        ZopeTestCase.installProduct('PasswordResetTool', quiet=1)
        ZopeTestCase.installProduct('PluggableAuthService', quiet=1)
        ZopeTestCase.installProduct('PluginRegistry', quiet=1)
        ZopeTestCase.installProduct('PlonePAS', quiet=1)
        ZopeTestCase.installProduct('kupu', quiet=1)
        # In Plone 2.5 we need the monkey-patch applied, starting
        # with Plone 3.0 it is part of CMFPlone.patches.
        try:
            from Products.PlacelessTranslationService import PatchStringIO
        except ImportError:
            pass

    if PLONE30:
        ZopeTestCase.installProduct('CMFEditions', quiet=1)
        ZopeTestCase.installProduct('CMFDiffTool', quiet=1)
        ZopeTestCase.installProduct('PloneLanguageTool', quiet=1)

    if PLONE40:
        ZopeTestCase.installProduct('TinyMCE', quiet=1)


def install_products_50():
    ZopeTestCase.installProduct('Archetypes', quiet=1)
    ZopeTestCase.installProduct('ATContentTypes', quiet=1)
    ZopeTestCase.installProduct('ATReferenceBrowserWidget', quiet=1)
    ZopeTestCase.installProduct('CMFCore', quiet=1)
    ZopeTestCase.installProduct('CMFDefault', quiet=1)
    ZopeTestCase.installProduct('CMFDynamicViewFTI', quiet=1)
    ZopeTestCase.installProduct('CMFFormController', quiet=1)
    ZopeTestCase.installProduct('CMFPlone', quiet=1)
    ZopeTestCase.installProduct('DCWorkflow', quiet=1)
    ZopeTestCase.installProduct('ExtendedPathIndex', quiet=1)
    ZopeTestCase.installProduct('MimetypesRegistry', quiet=1)
    ZopeTestCase.installProduct('PloneLanguageTool', quiet=1)
    ZopeTestCase.installProduct('PlonePAS', quiet=1)
    ZopeTestCase.installProduct('PluggableAuthService', quiet=1)
    ZopeTestCase.installProduct('PluginRegistry', quiet=1)
    ZopeTestCase.installProduct('PortalTransforms', quiet=1)
    ZopeTestCase.installProduct('ResourceRegistries', quiet=1)
    ZopeTestCase.installProduct('ZCTextIndex', quiet=1)

if PLONE50:
    install_products_50()
else:
    install_products()

ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('PageTemplates', quiet=1)
ZopeTestCase.installProduct('PythonScripts', quiet=1)
ZopeTestCase.installProduct('ExternalMethod', quiet=1)

# Check for layer support
try:
    import zope.testing.testrunner
except ImportError:
    try:
        import zope.testrunner
    except ImportError:
        USELAYER = 0
    else:
        USELAYER = 1
else:
    USELAYER = 1

# Check for Zope3 interfaces
try:
    from zope.interface.interfaces import IInterface
except ImportError:
    Z3INTERFACES = 0
else:
    from interfaces import IPloneTestCase
    Z3INTERFACES = IInterface.providedBy(IPloneTestCase)

# BBB: Zope 2.8
if PLONE25 and not USELAYER:
    ZopeTestCase.installProduct('Five', quiet=1)

from Testing.ZopeTestCase import transaction
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
from time import time
from Persistence import PersistentMapping

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

default_base_profile = 'CMFPlone:plone'
default_extension_profiles = ()

if PLONE30:
    default_base_profile = 'Products.CMFPlone:plone'

if PLONE40 and not PLONE50:
    default_extension_profiles = ('plonetheme.sunburst:default', )

if PLONE50:
    default_extension_profiles = ('Products.ATContentTypes:default', )

def setupPloneSite(id=portal_name,
                   policy=default_policy,
                   products=default_products,
                   quiet=0,
                   with_default_memberarea=1,
                   base_profile=default_base_profile,
                   extension_profiles=(),
                   default_extension_profiles=default_extension_profiles):
    '''Creates a Plone site and/or quickinstalls products into it.'''
    if USELAYER:
        quiet = 1
        cleanupPloneSite(id)
    if default_extension_profiles:
        extension_profiles = list(default_extension_profiles) + \
            list(extension_profiles)
    SiteSetup(id, policy, products, quiet, with_default_memberarea,
              base_profile, extension_profiles).run()

if USELAYER:
    import layer
    setupPloneSite = layer.onsetup(setupPloneSite)


def cleanupPloneSite(id):
    '''Removes a site.'''
    SiteCleanup(id).run()

if USELAYER:
    import layer
    cleanupPloneSite = layer.onteardown(cleanupPloneSite)


class SiteSetup:
    '''Creates a Plone site and/or quickinstalls products into it.'''

    def __init__(self, id, policy, products, quiet, with_default_memberarea,
                 base_profile, extension_profiles):
        self.id = id
        self.policy = policy
        self.products = products
        self.quiet = quiet
        self.with_default_memberarea = with_default_memberarea
        self.base_profile = base_profile
        self.extension_profiles = tuple(extension_profiles)

    def run(self):
        self.app = self._app()
        try:
            uf = self.app.acl_users
            if uf.getUserById(portal_owner) is None:
                # Add portal owner
                uf.userFolderAddUser(portal_owner, default_password, ['Manager'], [])
            if not hasattr(aq_base(self.app), self.id):
                # Add site
                self._login(uf, portal_owner)
                self._optimize()
                self._setupPackages()
                self._setupPloneSite()
                self._setupRegistries()
            if hasattr(aq_base(self.app), self.id):
                # Configure site
                self._login(uf, portal_owner)
                self._placefulSetUp()
                self._setupProfiles()
                self._setupProducts()
                # Pre-create default memberarea to speed up the tests
                if self.with_default_memberarea:
                    self._setupHomeFolder()
        finally:
            self._abort()
            self._placefulTearDown()
            self._close()
            self._logout()

    def _setupPloneSite(self):
        '''Creates the Plone site.'''
        if PLONE30:
            self._setupCreatedHook()
        if PLONE25:
            self._setupPloneSite_with_genericsetup()
        else:
            self._setupPloneSite_with_portalgenerator()

    def _setupPloneSite_with_genericsetup(self):
        '''Creates the site using GenericSetup.'''
        start = time()
        if self.base_profile != default_base_profile:
            self._print('Adding Plone Site (%s) ... ' % (self.base_profile,))
        else:
            self._print('Adding Plone Site ... ')
        # Add Plone site
        if PLONE40:
            from Products.CMFPlone.factory import addPloneSite
            addPloneSite(self.app, self.id, profile_id=self.base_profile)
        else:
            factory = self.app.manage_addProduct['CMFPlone']
            factory.addPloneSite(self.id, create_userfolder=1, snapshot=0,
                                 profile_id=self.base_profile)
        self._commit()
        self._print('done (%.3fs)\n' % (time()-start,))

    def _setupPloneSite_with_portalgenerator(self):
        '''Creates the site using PortalGenerator.'''
        start = time()
        if self.policy != default_policy:
            self._print('Adding Plone Site (%s) ... ' % (self.policy,))
        else:
            self._print('Adding Plone Site ... ')
        # Add Plone site
        factory = self.app.manage_addProduct['CMFPlone']
        factory.manage_addSite(self.id, create_userfolder=1, custom_policy=self.policy)
        self._commit()
        self._print('done (%.3fs)\n' % (time()-start,))

    def _setupRegistries(self):
        '''Installs persistent registries.'''
        portal = getattr(self.app, self.id)
        if not hasattr(portal, '_installed_profiles'):
            portal._installed_profiles = PersistentMapping()
            self._commit()

    def _setupProfiles(self):
        '''Imports extension profiles into the site.'''
        portal = getattr(self.app, self.id)
        setup = getattr(portal, 'portal_setup', None)
        if setup is not None:
            for profile in self.extension_profiles:
                if not portal._installed_profiles.has_key(profile):
                    start = time()
                    self._print('Adding %s ... ' % (profile,))
                    profile_id = 'profile-%s' % (profile,)
                    if PLONE30:
                        setup.runAllImportStepsFromProfile(profile_id)
                    else:
                        saved = setup.getImportContextID()
                        try:
                            setup.setImportContext(profile_id)
                            setup.runAllImportSteps()
                        finally:
                            setup.setImportContext(saved)
                    portal._installed_profiles[profile] = 1
                    self._commit()
                    self._print('done (%.3fs)\n' % (time()-start,))

    def _setupProducts(self):
        '''Quickinstalls products into the site.'''
        portal = getattr(self.app, self.id)
        qi = getattr(portal, 'portal_quickinstaller', None)
        if qi is None:
            self._print('Quick-installing products is not possible.\n')
            return

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

    def _setupPackages(self):
        '''Calls product-style initializer function for packages.'''
        if PLONE40:
            ZopeTestCase.installPackage('plone.app.imaging', quiet=1)
            ZopeTestCase.installPackage('plone.app.blob', quiet=1)
        if PLONE42:
            ZopeTestCase.installPackage('plone.app.collection', quiet=1)

    def _setupHomeFolder(self):
        '''Creates the default user's member folder.'''
        portal = getattr(self.app, self.id)
        _createHomeFolder(portal, default_user, take_ownership=0)
        self._commit()

    def _setupCreatedHook(self):
        '''Registers a handler for ISiteManagerCreatedEvent.'''
        from zope.component import getGlobalSiteManager
        from Products.CMFPlone.interfaces import ISiteManagerCreatedEvent
        gsm = getGlobalSiteManager()
        gsm.registerHandler(_placefulSetUpHandler, (ISiteManagerCreatedEvent,))

    def _placefulSetUp(self):
        '''Sets the local site/manager.'''
        if PLONE30:
            portal = getattr(self.app, self.id)
            _placefulSetUp(portal)

    def _placefulTearDown(self):
        '''Resets the local site/manager.'''
        if PLONE30:
            _placefulTearDown()

    def _optimize(self):
        '''Applies optimizations to the PortalGenerator.'''
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


class SiteCleanup(SiteSetup):
    '''Removes a site.'''

    def __init__(self, id):
        self.id = id

    def run(self):
        self.app = self._app()
        try:
            if hasattr(aq_base(self.app), self.id):
                self._placefulSetUp()
                self.app._delObject(self.id)
                self._commit()
        finally:
            self._abort()
            self._close()
            self._placefulTearDown()


def _placefulSetUpHandler(event):
    '''Subscriber for ISiteManagerCreatedEvent.
       Sets the local site/manager.
    '''
    portal = event.object
    _placefulSetUp(portal)


def _placefulSetUp(portal):
    '''Sets the local site/manager.'''
    try:
        from zope.site.hooks import setHooks, setSite
    except ImportError:
        from zope.app.component.hooks import setHooks, setSite
    setHooks()
    setSite(portal)


def _placefulTearDown():
    '''Resets the local site/manager.'''
    try:
        from zope.site.hooks import resetHooks, setSite
    except ImportError:
        from zope.app.component.hooks import resetHooks, setSite
    resetHooks()
    setSite()


def _createHomeFolder(portal, member_id, take_ownership=1):
    '''Creates a memberarea if it does not already exist.'''
    pm = portal.portal_membership
    members = pm.getMembersFolder()
    if members is None:
        _createObjectByType('Folder', portal, id='Members')
        members = portal.Members

    if not hasattr(aq_base(members), member_id):
        # Create home folder
        _createObjectByType('Folder', members, id=member_id)
        if not PLONE21:
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
        home.reindexObjectSecurity()
        if not PLONE21:
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
    # The site creation code is not needed anymore in Plone >= 2.5
    # as it is now based on GenericSetup
    if not PLONE25:
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
            if not PLONE21:
                p.Members.unindexObject()
        PloneGenerator.setupPortalContent = setupPortalContent
    # Don't populate type fields in the ConstrainTypesMixin schema
    if PLONE21:
        def _ct_defaultAddableTypeIds(self):
            return []
        from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixin
        ConstrainTypesMixin._ct_defaultAddableTypeIds = _ct_defaultAddableTypeIds

