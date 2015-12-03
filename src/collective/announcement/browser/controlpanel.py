"""
    Demo of the widget
    I haven't gotten these views working with tests.
"""
from five import grok

from zope.interface import Interface, implements
from zope import schema
from zope.schema.fieldproperty import FieldProperty
from zope.schema import getFieldsInOrder
from datetime import datetime

from z3c.form import field, button
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE, IDataConverter, NO_VALUE
from z3c.form.converter import BaseDataConverter

from plone.directives import form
from collective.z3cform.datagridfield.registry import DictRow
from collective.z3cform.datagridfield import DataGridFieldFactory, IDataGridField

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import RegistryEditForm
from Products.statusmessages.interfaces import IStatusMessage


class IAnnouncement(form.Schema):
    show_announcement = schema.Bool(
        title=u'Show the announcement',
        default=False,
        required=False,
    )
    show_on_all_pages = schema.Bool(
        title=u'Show on all pages',
        default=False,
        required=False,
    )
    expire_on = schema.Datetime(
        title=u'Expiration Date',
        required=False,
    )
    site_announcement = schema.Text(
        title=u'Message',
        required=False,
    )

class IAnnouncementForm(Interface):
    announcements = schema.List(title=u'Announcements',
        value_type=DictRow(title=u'Announcements', schema=IAnnouncement),
        required=True)


TESTDATA = {
    'announcements': [
           {'show_announcement': True,
            'show_on_all_pages': True,
            'expire_on': datetime.today(),
            'site_announcement': 'Mega City'
            }
    ]}
#-------------[ Views Follow ]-------------------------------------------

class AnnouncementControlPanelForm(RegistryEditForm):
    schema_prefix = "site_announcement"
    label = u'Announcement Settings'
    schema = IAnnouncementForm
    fields = field.Fields(IAnnouncementForm)
    fields['announcements'].widgetFactory = DataGridFieldFactory

    def updateActions(self):
        """Bypass the baseclass editform - it causes problems"""
        super(RegistryEditForm, self).updateActions()

    def updateWidgets(self):
        super(AnnouncementControlPanelForm, self).updateWidgets()
        self.widgets['announcements'].allow_reorder = True

    def getContent(self):
        data = super(AnnouncementControlPanelForm, self).getContent()
        if data:
            return data
        return TESTDATA

    @button.buttonAndHandler(u'Save', name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            "Changes saved.",
            "info")
        self.request.response.redirect(self.request.getURL())

AnnouncementControlPanelView = layout.wrap_form(
    AnnouncementControlPanelForm, ControlPanelFormWrapper)