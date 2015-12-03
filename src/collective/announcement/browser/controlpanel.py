# -*- coding: utf-8 -*-
from datetime import datetime
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from plone.app.textfield import RichText
from zope import schema
from zope.interface import Interface
from z3c.form.interfaces import INPUT_MODE
from z3c.form import field, form as z3c_form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone import api
from plone.directives import form
from zope.component import adapter
from plone.registry.interfaces import IRecordModifiedEvent
from five import grok

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow


class IAnnouncementRowSchema(Interface):
    show_announcement = schema.Bool(
        title=u'Show the announcement',
        description=u'The announcement is only displayed when this box is checked',
        default=False,
        required=False,
    )
    show_on_all_pages = schema.Bool(
        title=u'Show on all pages',
        description=u'Show on all pages not just the front page',
        default=False,
        required=False,
    )
    expire_on = schema.Datetime(
        title=u'Expiration Date',
        description=u'If set the announcement will be removed at this time',
        required=False,
    )
    site_announcement = schema.Text(
        title=u'An announcement that shows on the website',
        required=False,
    )

class IAnnouncementFormSchema(Interface):
    announcements = schema.List(title=u"Announcements",
        value_type=DictRow(title=u"tablerow", schema=IAnnouncementRowSchema))


class AnnouncementControlPanelForm(form.EditForm):
    label = u'Announcements List'
    z3c_form.extends(form.EditForm)

    grok.context(IAnnouncementFormSchema)
    grok.require('zope2.View')
    fields = field.Fields(IAnnouncementFormSchema)
    schema_prefix = "site_announcement"
    # this should give us a richtext widget for editing
    fields['announcements'].widgetFactory = DataGridFieldFactory
    
    #fields['site_announcement'].widgetFactory[INPUT_MODE] = WysiwygFieldWidget