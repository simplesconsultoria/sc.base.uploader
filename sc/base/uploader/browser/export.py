# -*- coding:utf-8 -*-
import os
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.i18n import translate

from collective.zipfiletransport.utilities.interfaces import IZipFileTransportUtility
from collective.zipfiletransport.browser.interfaces import IExport

from AccessControl import Unauthorized
from Acquisition import aq_parent, aq_inner
from OFS.interfaces import IOrderedContainer
from Products.ATContentTypes.interface import IATTopic
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView

from plone.memoize import view

import urllib


class ExportView(BrowserView):
    """ A browser view to export a folder as a zip file
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.zft_util = getUtility(
                            IZipFileTransportUtility, 
                            name="zipfiletransport")
    
    @view.memoize
    def _enable_anonymous(self):
        ''' Check if we enable anonymous download '''
        pp = getToolByName(self.context, 'portal_properties')
        sheet = pp.sc_base_uploader
        return sheet.getProperty("enable_export") or False
        
    def __call__(self,*args,**kwargs):
        ''' Return the zip file, if allowed '''
        
        # Anonymous enabled only if set globally
        if (self.context.portal_membership.isAnonymousUser() and not self._enable_anonymous()):
            return
        
        RESPONSE_BLOCK_SIZE = 32768
        # This would be great to filter content
        obj_paths = None
        
        context = self.context
        filename = '%s.zip' % (context.getId())
        
        zipfilename = self.zft_util.generateSafeFileName(filename)
        
        #Detect OS
        zipfilename = zipfilename.encode('utf-8')

        zip_path = self.zft_util.exportContent(
                                context=self.context,
                                obj_paths=obj_paths, 
                                filename=filename)

        self.context.REQUEST.RESPONSE.setHeader(
                                    'content-type', 
                                    'application/zip')
        self.context.REQUEST.RESPONSE.setHeader(
                                    'content-length', 
                                    str(os.stat(zip_path)[6]))
        self.context.REQUEST.RESPONSE.setHeader(
                                    'Content-Disposition',
                                    ' attachment; filename='+zipfilename)

        # iterate over the temporary file object, returning it to the client
        fp = open(zip_path, 'rb')
        while True:
            data = fp.read(RESPONSE_BLOCK_SIZE)
            if data:
                self.context.REQUEST.RESPONSE.write(data)
            else:
                break
        fp.close()
        # temporary measure to see the file object...
        os.rename(zip_path, zip_path + "_TEMP")
        return
    