#
# Tests a Plone Document
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Acquisition import aq_base

PloneTestCase.setupPloneSite()


class TestDocument(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.membership = self.portal.portal_membership
        self.folder.invokeFactory('Document', id='doc')

    def testAddDocument(self):
        self.failUnless(hasattr(aq_base(self.folder), 'doc'))
        self.failUnless(self.catalog(id='doc'))

    def testEditDocument(self):
        self.folder.doc.edit(text_format='plain', text='data')
        self.assertEqual(self.folder.doc.EditableBody(), 'data')

    def testReindexDocument(self):
        self.failIf(self.catalog(id='doc', Title='Foo'))
        self.folder.doc.setTitle('Foo')
        self.folder.doc.reindexObject()
        self.failUnless(self.catalog(id='doc', Title='Foo'))

    def testDeleteDocument(self):
        self.failUnless(self.catalog(id='doc'))
        self.folder._delObject('doc')
        self.failIf(self.catalog(id='doc'))

    def testSubmitDocument(self):
        self.workflow.doActionFor(self.folder.doc, 'submit')
        self.assertEqual(self.workflow.getInfoFor(self.folder.doc, 'review_state'), 'pending')
        self.failUnless(self.catalog(id='doc', review_state='pending'))

    def testRejectDocument(self):
        self.workflow.doActionFor(self.folder.doc, 'submit')
        self.setRoles(['Reviewer'])
        self.workflow.doActionFor(self.folder.doc, 'reject')
        self.assertEqual(self.workflow.getInfoFor(self.folder.doc, 'review_state'), 'visible')
        self.failUnless(self.catalog(id='doc', review_state='visible'))

    def testAcceptDocument(self):
        self.workflow.doActionFor(self.folder.doc, 'submit')
        self.setRoles(['Reviewer'])
        self.workflow.doActionFor(self.folder.doc, 'publish')
        self.assertEqual(self.workflow.getInfoFor(self.folder.doc, 'review_state'), 'published')
        self.failUnless(self.catalog(id='doc', review_state='published'))

    def testPublishDocument(self):
        self.setRoles(['Reviewer'])
        self.workflow.doActionFor(self.folder.doc, 'publish')
        self.assertEqual(self.workflow.getInfoFor(self.folder.doc, 'review_state'), 'published')
        self.failUnless(self.catalog(id='doc', review_state='published'))

    def testRetractDocument(self):
        self.setRoles(['Reviewer'])
        self.workflow.doActionFor(self.folder.doc, 'publish')
        self.setRoles(['Member'])
        self.workflow.doActionFor(self.folder.doc, 'retract')
        self.assertEqual(self.workflow.getInfoFor(self.folder.doc, 'review_state'), 'visible')
        self.failUnless(self.catalog(id='doc', review_state='visible'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDocument))
    return suite

if __name__ == '__main__':
    framework()

