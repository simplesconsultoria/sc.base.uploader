# -*- coding:utf-8 -*-
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.i18n import translate

from AccessControl import Unauthorized
from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName

from plone.memoize import instance

# Forms Interfaces
from collective.quickupload.browser.quickupload_settings import IQuickUploadControlPanel
from collective.zipfiletransport.browser.zipfiletransportprefs import IZipFileTransportPrefsForm

from zope.formlib.form import FormFields
from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

from sc.base.uploader import MessageFactory as _

quickset = FormFieldsets(IQuickUploadControlPanel)
quickset.id = 'quickupload'
quickset.label = _(u'Quick Upload settings')

zipset = FormFieldsets(IZipFileTransportPrefsForm)
zipset.id = 'ziptransport'
zipset.label = _(u'ZipFileTransport Settings Form')

class ConfigletView(ControlPanelForm):
    """ A browser view to configure uploader
    """
    form_fields = FormFieldsets(quickset, zipset)

    label = _(u"Multiple files upload")
    description = _(u"Control settings for multiple file upload.")
    form_name = _("Multiple files upload")
    