
PloneTestCase Readme

    PloneTestCase is a thin layer on top of the ZopeTestCase package. It has
    been developed to simplify testing of Plone-based applications and products.


    The PloneTestCase package provides:

        - The method installProduct() to install a Zope product into the 
          test environment.

        - The method setupPloneSite() to create a Plone portal in the test db.

        - The utils module known from the ZopeTestCase package.

        - The PloneTestCase base class of which to derive your test cases.

        - The FunctionalTestCase base class of which to derive your test 
          cases for functional unit tests.


    Example PloneTestCase::

        from Products.PloneTestCase import PloneTestCase

        PloneTestCase.installProduct('SomeProduct')
        PloneTestCase.setupPloneSite()

        class TestSomething(PloneTestCase.PloneTestCase):

            def afterSetup(self):
                self.folder.invokeFactory('Document', 'doc')

            def testEditDocument(self):
                self.folder.doc.edit(text_format='plain', text='data')
                self.assertEqual(self.folder.doc.EditableBody(), 'data')


    Please see the docs of the ZopeTestCase package, especially those 
    about the PortalTestCase class. 

    Look at the example tests in this directory to get an idea of how 
    to use the PloneTestCase package. Also see the tests coming with
    Plone 2.x.

    Copy testSkeleton.py to start your own tests.

