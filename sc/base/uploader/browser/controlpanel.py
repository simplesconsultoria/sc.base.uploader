# -*- coding:utf-8 -*-
from zope.component import getMultiAdapter
from zope.component import adapts
from zope.interface import Interface, implements
from zope.i18n import translate
from zope import schema

from AccessControl import Unauthorized
from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot

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

class IExporterPrefsForm(Interface):    
    """ A configlet for exporting content. """
    
    enable_export = schema.Bool(title=_(u"Enable anonymous export"),
                           description=_(u"Should exporting contents from a folder be enabled for anonymous users?"),
                           default=False,
                           required=False)

class ExporterCPAdapter(SchemaAdapterBase):
    
    adapts(IPloneSiteRoot)
    implements(IExporterPrefsForm)

    def __init__(self, context):
        super(ExporterCPAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.sc_base_uploader

    enable_export = ProxyFieldProperty(IExporterPrefsForm['enable_export'])

exportset = FormFieldsets(IExporterPrefsForm)
exportset.id = 'exporter'
exportset.label = _(u'Export Settings Form')

class ConfigletView(ControlPanelForm):
    """ A browser view to configure uploader
    """
    form_fields = FormFieldsets(quickset, zipset,exportset)

    label = _(u"Multiple files upload")
    description = _(u"Control settings for multiple file upload.")
    form_name = _("Multiple files upload")
    