from setuptools import setup, find_packages
import os

version = '1.0.0dev'

setup(name='Products.PloneTestCase',
      version=version,
      description="Integration testing framework for Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
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
      install_requires=[
          'setuptools',
          'zope.interface',
          'Products.CMFPlone',
          'zope.app.component',
          'Products.CMFCore',
          'Products.ATContentTypes',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
