import sys
from setuptools import setup, find_packages

version = '0.9.14'

# We only specify our real dependencies when run with Python 2.6.
# This is to ensure backwards compatibility with older Plone versions which
# do not yet allow specifying these
if sys.version_info[:3] >= (2,6,0):
    install_requires=[
        'setuptools',
        'zope.component',
        'zope.interface',
        'zope.site',
        'zope.testing',
        'Acquisition',
        'Products.CMFPlone',
        'Products.ATContentTypes',
        'Products.CMFCore',
        'Products.GenericSetup',
        'ZODB3',
        'Zope2',
    ]
else:
    install_requires=[
        'setuptools',
    ]

setup(name='Products.PloneTestCase',
      version=version,
      description="Integration testing framework for Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone testing',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='http://plone.org/products/plonetestcase',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
)
