# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from sc.base.uploader.config import PRODUCTS


def upgrade0to1(context):
    ''' Upgrade to version 1.0
    '''
    qi = getToolByName(context, 'portal_quickinstaller')

    # Install dependencies for this upgrade
    # List package names
    packages = ['collective.quickupload',
                'collective.zipfiletransport']
    # (name,locked,hidden,install,profile,runProfile)
    dependencies = [(name, locked, hidden, profile)
                    for name, locked, hidden, install,
                    profile, runProfile in PRODUCTS
                    if ((name in packages) and install)]

    for name, locked, hidden, profile in dependencies:
        qi.installProduct(name, locked=locked, hidden=hidden, profile=profile)
