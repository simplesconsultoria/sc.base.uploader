# -*- coding: utf-8 -*-
from plone.app.testing import logout
from Products.CMFCore.utils import getToolByName
from sc.base.uploader.testing import INTEGRATION_TESTING
from zope.component import getMultiAdapter

import unittest2 as unittest


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='uploader-controlpanel')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_protected(self):
        # control panel view can not be accessed by anonymous users
        from AccessControl import Unauthorized
        logout()
        portal = self.portal
        self.assertRaises(Unauthorized,
                          portal.restrictedTraverse, '@@uploader-controlpanel')

    def test_configlet_install(self):
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        installed = [a.getAction(self)['id']
                     for a in controlpanel.listActions()]
        self.failUnless('uploader-config' in installed)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
