#
# Tests the membership tool
#

import os
import sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Acquisition import aq_base
from AccessControl.User import nobody

PloneTestCase.setupPloneSite()
default_user = PloneTestCase.default_user

if PloneTestCase.PLONE25:
    USERFOLDER = 'PluggableAuthService'
    USERTYPE = 'PloneUser'
else:
    USERFOLDER = 'GroupUserFolder'
    USERTYPE = 'GRUFUser'

try:
    from zExceptions import BadRequest
except ImportError:
    BadRequest = 'BadRequest'


class TestMembershipTool(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.membership = self.portal.portal_membership
        self.membership.memberareaCreationFlag = 1
        self.membership.addMember('user2', 'secret', ['Member'], [])

    def testAddMember(self):
        self.assertTrue(self.portal.acl_users.getUserById('user2'))

    def testAddMemberIfMemberExists(self):
        # Nothing should happen
        self.membership.addMember('user2', 'secret', ['Member'], [])
        self.assertTrue(self.portal.acl_users.getUserById('user2'))

    def testGetMemberById(self):
        user = self.membership.getMemberById(default_user)
        self.assertEqual(user, None)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, USERTYPE)

    def testListMemberIds(self):
        ids = self.membership.listMemberIds()
        self.assertEqual(len(ids), 2)
        self.assertTrue(default_user in ids)
        self.assertTrue('user2' in ids)

    def testListMembers(self):
        members = self.membership.listMembers()
        self.assertEqual(len(members), 2)
        self.assertEqual(members[0].__class__.__name__, 'MemberData')
        self.assertEqual(members[0].aq_parent.__class__.__name__, USERTYPE)
        self.assertEqual(members[1].__class__.__name__, 'MemberData')
        self.assertEqual(members[1].aq_parent.__class__.__name__, USERTYPE)

    def testGetAuthenticatedMember(self):
        member = self.membership.getAuthenticatedMember()
        self.assertEqual(member.getUserName(), default_user)

    def testGetAuthenticatedMemberIfAnonymous(self):
        self.logout()
        member = self.membership.getAuthenticatedMember()
        self.assertEqual(member.getUserName(), 'Anonymous User')

    def testIsAnonymousUser(self):
        self.assertFalse(self.membership.isAnonymousUser())
        self.logout()
        self.assertTrue(self.membership.isAnonymousUser())

    if PloneTestCase.PLONE25:

        def testSetPassword(self):
            # PAS does not provide the password
            self.membership.setPassword('geheim')
            member = self.membership.getMemberById(default_user)
            #self.assertEqual(member.getPassword(), 'geheim')
            self.assertEqual(member.getPassword(), None)

    else:

        def testSetPassword(self):
            self.membership.setPassword('geheim')
            member = self.membership.getMemberById(default_user)
            self.assertEqual(member.getPassword(), 'geheim')

    def testSetPasswordIfAnonymous(self):
        self.logout()
        try:
            self.membership.setPassword('geheim')
        except BadRequest:
            pass
        except:
            # String exceptions suck
            e, v, tb = sys.exc_info()
            del tb
            if str(v) == 'Bad Request':
                pass
        else:
            self.fail('Anonymous can change password')

    def testWrapUserWrapsBareUser(self):
        user = self.portal.acl_users.getUserById(default_user)
        # XXX: GRUF users are wrapped
        self.assertTrue(hasattr(user, 'aq_base'))
        user = aq_base(user)
        user = self.membership.wrapUser(user)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, USERTYPE)
        self.assertEqual(user.aq_parent.aq_parent.__class__.__name__,
                         USERFOLDER)

    def testWrapUserWrapsWrappedUser(self):
        user = self.portal.acl_users.getUserById(default_user)
        # XXX: GRUF users are wrapped
        self.assertTrue(hasattr(user, 'aq_base'))
        user = self.membership.wrapUser(user)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, USERTYPE)
        self.assertEqual(user.aq_parent.aq_parent.__class__.__name__,
                         USERFOLDER)

    def testWrapUserDoesntWrapMemberData(self):
        user = self.portal.acl_users.getUserById(default_user)
        user.getMemberId = lambda x: 1
        user = self.membership.wrapUser(user)
        self.assertEqual(user.__class__.__name__, USERTYPE)

    def testWrapUserWrapsAnonymous(self):
        self.assertFalse(hasattr(nobody, 'aq_base'))
        user = self.membership.wrapUser(nobody, wrap_anon=1)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, 'SpecialUser')
        self.assertEqual(user.aq_parent.aq_parent.__class__.__name__,
                         USERFOLDER)

    def testWrapUserDoesntWrapAnonymous(self):
        user = self.membership.wrapUser(nobody)
        self.assertEqual(user.__class__.__name__, 'SpecialUser')

    if PloneTestCase.PLONE30:

        def testGetPortalRoles(self):
            roles = self.membership.getPortalRoles()
            self.assertTrue(len(roles) >= 7)
            self.assertTrue('Manager' in roles)
            self.assertTrue('Member' in roles)
            self.assertTrue('Owner' in roles)
            self.assertTrue('Reviewer' in roles)
            self.assertTrue('Reader' in roles)
            self.assertTrue('Editor' in roles)
            self.assertTrue('Contributor' in roles)

    else:

        def testGetPortalRoles(self):
            roles = self.membership.getPortalRoles()
            self.assertEqual(len(roles), 4)
            self.assertTrue('Manager' in roles)
            self.assertTrue('Member' in roles)
            self.assertTrue('Owner' in roles)
            self.assertTrue('Reviewer' in roles)

    def testSetRoleMapping(self):
        self.membership.setRoleMapping('Reviewer', 'FooRole')
        self.assertEqual(self.membership.role_map['Reviewer'], 'FooRole')

    def testGetMappedRole(self):
        self.membership.setRoleMapping('Reviewer', 'FooRole')
        self.assertEqual(self.membership.getMappedRole('Reviewer'), 'FooRole')

    # XXX: Plone does not map roles
    #def testWrapUserMapsRoles(self):
    #    self.membership.setRoleMapping('Reviewer', 'FooRole')
    #    self.setRoles(['FooRole'])
    #    user = self.portal.acl_users.getUserById(default_user)
    #    user = self.membership.wrapUser(user)
    #    self.assertEqual(user.getRoles(),
    #                     ('FooRole', 'Reviewer', 'Authenticated'))

    def testMemberareaCreationFlag(self):
        self.assertTrue(self.membership.getMemberareaCreationFlag())

    if PloneTestCase.PLONE21:

        def testCreateMemberarea(self):
            # CMF 1.5 requires user2 to be logged in!
            self.login('user2')
            members = self.membership.getMembersFolder()
            self.assertFalse(hasattr(aq_base(members), 'user2'))
            self.membership.createMemberArea('user2')
            self.assertTrue(hasattr(aq_base(members), 'user2'))

        def testCreateMemberareaIfDisabled(self):
            # No longer works in CMF 1.5
            self.membership.setMemberareaCreationFlag()  # toggle
            members = self.membership.getMembersFolder()
            self.assertFalse(hasattr(aq_base(members), 'user2'))
            self.membership.createMemberArea('user2')
            #self.assertTrue(hasattr(aq_base(members), 'user2'))
            self.assertFalse(hasattr(aq_base(members), 'user2'))

        def testWrapUserCreatesMemberarea(self):
            # No longer the case in CMF 1.5
            members = self.membership.getMembersFolder()
            user = self.portal.acl_users.getUserById('user2')
            user = self.membership.wrapUser(user)
            #self.assertTrue(hasattr(aq_base(members), 'user2'))
            self.assertFalse(hasattr(aq_base(members), 'user2'))

    else:

        def testCreateMemberarea(self):
            members = self.membership.getMembersFolder()
            self.assertFalse(hasattr(aq_base(members), 'user2'))
            self.membership.createMemberarea('user2')
            self.assertTrue(hasattr(aq_base(members), 'user2'))

        def testCreateMemberareaIfDisabled(self):
            # This should work even if the flag is off
            self.membership.setMemberareaCreationFlag()  # toggle
            members = self.membership.getMembersFolder()
            self.assertFalse(hasattr(aq_base(members), 'user2'))
            self.membership.createMemberarea('user2')
            self.assertTrue(hasattr(aq_base(members), 'user2'))

        def testWrapUserCreatesMemberarea(self):
            members = self.membership.getMembersFolder()
            user = self.portal.acl_users.getUserById('user2')
            user = self.membership.wrapUser(user)
            self.assertTrue(hasattr(aq_base(members), 'user2'))

    def testWrapUserDoesntCreateMemberarea(self):
        # No member area is created if the flag is off
        self.membership.setMemberareaCreationFlag()
        members = self.membership.getMembersFolder()
        user = self.portal.acl_users.getUserById('user2')
        user = self.membership.wrapUser(user)
        self.assertFalse(hasattr(aq_base(members), 'user2'))

    def testGetCandidateLocalRoles(self):
        self.assertEqual(self.membership.getCandidateLocalRoles(self.folder),
                         ('Owner',))
        self.setRoles(['Member', 'Reviewer'])
        self.assertEqual(self.membership.getCandidateLocalRoles(self.folder),
                         ('Owner', 'Reviewer'))

    def testSetLocalRoles(self):
        self.assertTrue(
            'Owner' in self.folder.get_local_roles_for_userid(default_user))
        self.setRoles(['Member', 'Reviewer'])
        self.membership.setLocalRoles(self.folder, [default_user, 'user2'],
                                      'Reviewer')
        self.assertEqual(self.folder.get_local_roles_for_userid(default_user),
                         ('Owner', 'Reviewer'))
        self.assertEqual(self.folder.get_local_roles_for_userid('user2'),
                         ('Reviewer',))

    def testDeleteLocalRoles(self):
        self.setRoles(['Member', 'Reviewer'])
        self.membership.setLocalRoles(self.folder, ['user2'], 'Reviewer')
        self.assertEqual(self.folder.get_local_roles_for_userid('user2'),
                         ('Reviewer',))
        self.membership.deleteLocalRoles(self.folder, ['user2'])
        self.assertEqual(self.folder.get_local_roles_for_userid('user2'), ())

    def testGetHomeFolder(self):
        self.assertEqual(self.membership.getHomeFolder(), None)
        self.assertEqual(self.membership.getHomeFolder('user2'), None)

    def testGetHomeUrl(self):
        self.assertEqual(self.membership.getHomeUrl(), None)
        self.assertEqual(self.membership.getHomeUrl('user2'), None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembershipTool))
    return suite

if __name__ == '__main__':
    framework()
