# -*- coding:utf-8 -*-
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.i18n import translate

from AccessControl import Unauthorized
from Acquisition import aq_parent, aq_inner
from OFS.interfaces import IOrderedContainer
from Products.ATContentTypes.interface import IATTopic
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView

from plone.memoize import instance

from Products.CMFPlone.interfaces import IPloneSiteRoot

import urllib


class ImportView(BrowserView):
    """ A browser view to mass import contents
    """
    
    