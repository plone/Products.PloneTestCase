#
# Tests the membership tool
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Acquisition import aq_base
from AccessControl.User import nobody

PloneTestCase.setupPloneSite()
default_user = PloneTestCase.default_user

from zExceptions import BadRequest


class TestMembershipTool(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.membership = self.portal.portal_membership
        self.membership.addMember('user2', 'secret', ['Member'], [])

    def testAddMember(self):
        self.failUnless(self.portal.acl_users.getUserById('user2'))

    def testAddMemberIfMemberExists(self):
        # Nothing should happen
        self.membership.addMember('user2', 'secret', ['Member'], [])
        self.failUnless(self.portal.acl_users.getUserById('user2'))

    def testGetMemberById(self):
        user = self.membership.getMemberById(default_user)
        self.failIfEqual(user, None)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, 'GRUFUser')

    def testListMemberIds(self):
        ids = self.membership.listMemberIds()
        self.assertEqual(len(ids), 2)
        self.failUnless(default_user in ids)
        self.failUnless('user2' in ids)

    def testListMembers(self):
        members = self.membership.listMembers()
        self.assertEqual(len(members), 2)
        self.assertEqual(members[0].__class__.__name__, 'MemberData')
        self.assertEqual(members[0].aq_parent.__class__.__name__, 'GRUFUser')
        self.assertEqual(members[1].__class__.__name__, 'MemberData')
        self.assertEqual(members[1].aq_parent.__class__.__name__, 'GRUFUser')

    def testGetAuthenticatedMember(self):
        member = self.membership.getAuthenticatedMember()
        self.assertEqual(member.getUserName(), default_user)

    def testGetAuthenticatedMemberIfAnonymous(self):
        self.logout()
        member = self.membership.getAuthenticatedMember()
        self.assertEqual(member.getUserName(), 'Anonymous User')

    def testIsAnonymousUser(self):
        self.failIf(self.membership.isAnonymousUser())
        self.logout()
        self.failUnless(self.membership.isAnonymousUser())

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
            e,v,tb = sys.exc_info(); del tb
            raise
        else:
            self.fail('Anonymous can change password')

    def testWrapUserWrapsBareUser(self):
        user = self.portal.acl_users.getUserById(default_user)
        # XXX: GRUF users are wrapped
        self.failUnless(hasattr(user, 'aq_base'))
        user = aq_base(user)
        user = self.membership.wrapUser(user)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, 'GRUFUser')
        self.assertEqual(user.aq_parent.aq_parent.__class__.__name__, 'GroupUserFolder')

    def testWrapUserWrapsWrappedUser(self):
        user = self.portal.acl_users.getUserById(default_user)
        # XXX: GRUF users are wrapped
        self.failUnless(hasattr(user, 'aq_base'))
        user = self.membership.wrapUser(user)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, 'GRUFUser')
        self.assertEqual(user.aq_parent.aq_parent.__class__.__name__, 'GroupUserFolder')

    def testWrapUserDoesntWrapMemberData(self):
        user = self.portal.acl_users.getUserById(default_user)
        user.getMemberId = lambda x: 1
        user = self.membership.wrapUser(user)
        self.assertEqual(user.__class__.__name__, 'GRUFUser')

    def testWrapUserWrapsAnonymous(self):
        self.failIf(hasattr(nobody, 'aq_base'))
        user = self.membership.wrapUser(nobody, wrap_anon=1)
        self.assertEqual(user.__class__.__name__, 'MemberData')
        self.assertEqual(user.aq_parent.__class__.__name__, 'SpecialUser')
        self.assertEqual(user.aq_parent.aq_parent.__class__.__name__, 'GroupUserFolder')

    def testWrapUserDoesntWrapAnonymous(self):
        user = self.membership.wrapUser(nobody)
        self.assertEqual(user.__class__.__name__, 'SpecialUser')

    def testGetPortalRoles(self):
        roles = self.membership.getPortalRoles()
        self.assertEqual(len(roles), 4)
        self.failUnless('Manager' in roles)
        self.failUnless('Member' in roles)
        self.failUnless('Owner' in roles)
        self.failUnless('Reviewer' in roles)

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
    #    self.assertEqual(user.getRoles(), ('FooRole', 'Reviewer', 'Authenticated'))

    def testMemberareaCreationFlag(self):
        self.failUnless(self.membership.getMemberareaCreationFlag())

    def testCreateMemberarea(self):
        members = self.membership.getMembersFolder()
        self.failIf(hasattr(aq_base(members), 'user2'))
        self.membership.createMemberarea('user2')
        self.failUnless(hasattr(aq_base(members), 'user2'))

    def testCreateMemberareaIfDisabled(self):
        # This should work even if the flag is off
        self.membership.setMemberareaCreationFlag()
        members = self.membership.getMembersFolder()
        self.failIf(hasattr(aq_base(members), 'user2'))
        self.membership.createMemberarea('user2')
        self.failUnless(hasattr(aq_base(members), 'user2'))

    def testWrapUserCreatesMemberarea(self):
        members = self.membership.getMembersFolder()
        user = self.portal.acl_users.getUserById('user2')
        user = self.membership.wrapUser(user)
        self.failUnless(hasattr(aq_base(members), 'user2'))

    def testWrapUserDoesntCreateMemberarea(self):
        # No member area is created if the flag is off
        self.membership.setMemberareaCreationFlag()
        members = self.membership.getMembersFolder()
        user = self.portal.acl_users.getUserById('user2')
        user = self.membership.wrapUser(user)
        self.failIf(hasattr(aq_base(members), 'user2'))

    def testGetCandidateLocalRoles(self):
        self.assertEqual(self.membership.getCandidateLocalRoles(self.folder), ('Owner',))
        self.setRoles(['Member', 'Reviewer'])
        self.assertEqual(self.membership.getCandidateLocalRoles(self.folder), ('Owner', 'Reviewer'))

    def testSetLocalRoles(self):
        self.failUnless('Owner' in self.folder.get_local_roles_for_userid(default_user))
        self.setRoles(['Member', 'Reviewer'])
        self.membership.setLocalRoles(self.folder, [default_user, 'user2'], 'Reviewer')
        self.assertEqual(self.folder.get_local_roles_for_userid(default_user), ('Owner', 'Reviewer'))
        self.assertEqual(self.folder.get_local_roles_for_userid('user2'), ('Reviewer',))

    def testDeleteLocalRoles(self):
        self.setRoles(['Member', 'Reviewer'])
        self.membership.setLocalRoles(self.folder, ['user2'], 'Reviewer')
        self.assertEqual(self.folder.get_local_roles_for_userid('user2'), ('Reviewer',))
        self.membership.deleteLocalRoles(self.folder, ['user2'])
        self.assertEqual(self.folder.get_local_roles_for_userid('user2'), ())

    def testGetHomeFolder(self):
        self.failIfEqual(self.membership.getHomeFolder(), None)
        self.assertEqual(self.membership.getHomeFolder('user2'), None)

    def testGetHomeUrl(self):
        self.failIfEqual(self.membership.getHomeUrl(), None)
        self.assertEqual(self.membership.getHomeUrl('user2'), None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembershipTool))
    return suite

if __name__ == '__main__':
    framework()

