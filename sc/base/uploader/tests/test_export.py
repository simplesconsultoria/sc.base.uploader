# -*- coding: utf-8 -*-
import os
import unittest2 as unittest

from zope.app.component.hooks import getSite

from plone.testing.z2 import Browser

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from sc.base.uploader.testing import FUNCTIONAL_TESTING


class ExportTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUpContent(self):
        self.portal.invokeFactory('Folder',
                                  'f1',
                                  title=u"Folder 1")
        self.folder = self.portal['f1']
        files = ['test_image.png', 'test_image.jpg', ]
        for filename in files:
            image_file = open(os.path.join(os.path.dirname(__file__),
                              filename))
            self.folder.invokeFactory('Image', filename)
            image = self.folder[filename]
            image.setImage(image_file.read())
            image.reindexObject()

    def setUp(self):
        self.app = self.layer['app']        
        self.portal = self.layer['portal']
        self.pp = self.portal['portal_properties']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setUpContent()
        self.browser = Browser(self.app)
        # Persist changes in ZODB
        import transaction
        transaction.commit()

    def test_export_content_type(self):
        url = self.folder.absolute_url()
        browser = self.browser
        browser.addHeader('Authorization', 'Basic %s:%s' %
                          (TEST_USER_NAME, TEST_USER_PASSWORD,))
        browser.open('%s/@@export-zip' % url)
        self.assertEqual(browser.headers['content-type'], 'application/zip')

    def test_export_filename(self):
        url = self.folder.absolute_url()
        browser = self.browser
        browser.addHeader('Authorization', 'Basic %s:%s' %
                          (TEST_USER_NAME, TEST_USER_PASSWORD,))
        browser.open('%s/@@export-zip' % url)
        self.assertEqual(browser.headers['Content-Disposition'],
                         'attachment; filename=f1.zip')

    def test_export_cache(self):
        url = self.folder.absolute_url()
        browser = self.browser
        browser.addHeader('Authorization', 'Basic %s:%s' %
                          (TEST_USER_NAME, TEST_USER_PASSWORD,))
        browser.open('%s/@@export-zip' % url)
        self.assertEqual(browser.headers['X-Cache-Rule'],
                         'zip-exporsct-42')
        self.assertEqual(browser.headers['Cache-Control'],
                         'max-age=86400, proxy-revalidate, public')

    def test_anonymous_export(self):
        # Enable anonymous export
        props = self.pp.sc_base_uploader
        props.manage_changeProperties(enable_export=True)
        import transaction
        transaction.commit()
        # Proceed with the testing
        url = self.folder.absolute_url()
        browser = self.browser
        browser.open('%s/@@export-zip' % url)
        self.assertEqual(browser.headers['Content-Disposition'],
                         'attachment; filename=f1.zip')
        self.assertEqual(browser.headers['X-Cache-Rule'],
                         'zip-exporsct-42')
        self.assertEqual(browser.headers['Cache-Control'],
                         'max-age=86400, proxy-revalidate, public')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
