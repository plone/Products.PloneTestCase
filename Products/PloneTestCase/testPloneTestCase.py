#
# Tests the PloneTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Acquisition import aq_base

PloneTestCase.setupPloneSite()
default_user = PloneTestCase.default_user


class TestPloneTestCase(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.membership = self.portal.portal_membership

    def testDefaultMemberarea(self):
        self.assertEqual(self.folder.getOwner().getId(), default_user)
        self.assertEqual(self.folder.get_local_roles_for_userid(default_user), ('Owner',))
        self.failUnless(hasattr(aq_base(self.folder), '.personal'))
        # XXX: PloneFolders always have an index_html attribute
        #self.failIf(hasattr(aq_base(self.folder), 'index_html'))

    def testCreateMemberarea(self):
        self.membership.addMember('user2', 'secret', [], [])
        self.createMemberarea('user2')
        home = self.membership.getHomeFolder('user2')
        self.assertEqual(home.getOwner().getId(), 'user2')
        self.assertEqual(home.get_local_roles_for_userid('user2'), ('Owner',))
        self.assertEqual(home.get_local_roles_for_userid(default_user), ())
        self.failUnless(hasattr(aq_base(self.folder), '.personal'))
        # XXX: PloneFolders always have an index_html attribute
        #self.failIf(hasattr(aq_base(home), 'index_html'))

    def testAddDocument(self):
        self.folder.invokeFactory('Document', id='doc')
        self.failUnless(hasattr(aq_base(self.folder), 'doc'))

    def testEditDocument(self):
        self.folder.invokeFactory('Document', id='doc')
        self.folder.doc.edit(text_format='plain', text='data')
        self.assertEqual(self.folder.doc.EditableBody(), 'data')

    def testPublishDocument(self):
        self.folder.invokeFactory('Document', id='doc')
        self.setRoles(['Reviewer'])
        self.workflow.doActionFor(self.folder.doc, 'publish')
        self.assertEqual(self.workflow.getInfoFor(self.folder.doc, 'review_state'), 'published')
        self.failUnless(self.catalog(id='doc', review_state='published'))

    def testSkinScript(self):
        self.folder.invokeFactory('Document', id='doc', title='Foo')
        self.assertEqual(self.folder.doc.TitleOrId(), 'Foo')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneTestCase))
    return suite

if __name__ == '__main__':
    framework()

