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

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow


class IAnnouncement(Interface):
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


class IAnnouncementList(schema.List):
    pass


class IAnnouncementForm(Interface):
    announcements = IAnnouncementList(title=u"Announcements",
        value_type=schema.Object(title=u"Announcement",
                                 schema=IAnnouncement))


class IAddress(Interface):
    address_type = schema.Choice(
        title = u'Address Type', required=True,
        values=[u'Work', u'Home'])
    line1 = schema.TextLine(
        title = u'Line 1', required=True)
    line2 = schema.TextLine(
        title = u'Line 2', required=False)
    city = schema.TextLine(
        title = u'City / Town', required=True)
    country = schema.TextLine(
        title = u'Country', required=True)

class AddressListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

class IPerson(Interface):
    name = schema.TextLine(title=u'Name', required=True)
    address = AddressListField(title=u'Addresses',
        value_type=schema.Object(title=u'Address', schema=IAddress),
        required=True)

class Address(object):
    implements(IAddress)
    address_type = FieldProperty(IAddress['address_type'])
    line1 = FieldProperty(IAddress['line1'])
    line2 = FieldProperty(IAddress['line2'])
    city = FieldProperty(IAddress['city'])
    country = FieldProperty(IAddress['country'])

    def __init__(self, address_type=None, line1=None, line2=None, city=None, country=None):
        self.address_type = address_type
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.country = country

class AddressList(list):
    pass

class Person(object):
    implements(IPerson)
    name = FieldProperty(IPerson['name'])
    address = FieldProperty(IPerson['address'])

    def __init__(self, name=None, address=None):
        self.name = name
        self.address = address

TESTDATA = Person(
    name = u'MY NAME',
    address = AddressList([
        Address(address_type = u'Work',
            line1 = u'My Office',
            line2 = u'Big Office Block',
            city = u'Mega City',
            country = u'The Old Sod'),
        Address(address_type = u'Home',
            line1 = u'Home Sweet Home',
            line2 = u'Easy Street',
            city = u'Burbs',
            country = u'The Old Sod')
    ]))

class AnnouncementControlPanelForm(form.EditForm):
    
    label = u'Announcements List'
    fields = field.Fields(IAnnouncementForm)
    schema_prefix = "site_announcement"
    # this should give us a richtext widget for editing
    fields['announcements'].widgetFactory = DataGridFieldFactory
       
    #fields['site_announcement'].widgetFactory[INPUT_MODE] = WysiwygFieldWidget

AnnouncementControlPanelView = layout.wrap_form(
    AnnouncementControlPanelForm, ControlPanelFormWrapper)