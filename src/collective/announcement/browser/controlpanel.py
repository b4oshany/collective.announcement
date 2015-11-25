# -*- coding: utf-8 -*-
from datetime import datetime
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from plone.app.textfield import RichText
from zope import schema
from zope.interface import Interface
from z3c.form.interfaces import INPUT_MODE
from z3c.form import form, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone import api

from zope.component import adapter
from plone.registry.interfaces import IRecordModifiedEvent


class IAnnouncementControlPanel(Interface):

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


class AnnouncementControlPanelForm(RegistryEditForm):
    fields = field.Fields(IAnnouncementControlPanel)
    # this should give us a richtext widget for editing
    fields['site_announcement'].widgetFactory[INPUT_MODE] = WysiwygFieldWidget
    schema = IAnnouncementControlPanel
    schema_prefix = "site_announcement"
    label = u'Announcement Settings'


AnnouncementControlPanelView = layout.wrap_form(
    AnnouncementControlPanelForm, ControlPanelFormWrapper)


@adapter(IAnnouncementControlPanel, IRecordModifiedEvent)
def handleRegistryModified(settings, event):
    if event.record.fieldName in ['site_announcement', 'expire_on']:
        api.portal.set_registry_record('site_announcement.date_updated',
                                       datetime.now())

