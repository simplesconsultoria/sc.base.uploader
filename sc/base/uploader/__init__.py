# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory as BaseMessageFactory
MessageFactory = BaseMessageFactory('sc.base.uploader')

from sc.base.uploader import patch

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

patch.run()